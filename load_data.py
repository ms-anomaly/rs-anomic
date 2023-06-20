import pandas as pd
import constants
import torch

def get_data(path,path_rt,size,anomaly=''):
  dfs = dict()
  print('get data: ',anomaly)
  for j,service in enumerate(services):

    if anomaly!='':
      path_ = path+anomaly+'/'+service+'.csv'
    else:
      path_ = path+service+'.csv'

    try:
      data = pd.read_csv(path_)
      dataframe = pd.DataFrame(data)
      df = dataframe.loc[:, cols]
      df = df.interpolate(method ='linear', limit_direction ='both')
      #df = df.fillna(method='ffill')
      #df = df.fillna(method='bfill')

      for col in df:
        if col in cumulative_cols:
          df[col] = df[col].diff()
          df[col].loc[df[col] < 0] = 0
      df = df.drop([0,1,2],axis=0)

    except Exception as e:
      print('error: ',e)
      print(path_)
      df = pd.DataFrame(0.000001, index=range(size), columns=cols)
    dfs[service] = df
  t = []
  for i in services:
    t.append(torch.tensor(dfs[i].values.tolist())[:size])


  dfs_rt = dict()
  for j,service in enumerate(containers):
    if len(rt_per_service[service]) ==0:
      continue
    if anomaly!='':
      path_rt_ = path_rt+anomaly+'_rt/'+service+'.csv'
    else:
      path_rt_ = path_rt+service+'.csv'
    try:
      data = pd.read_csv(path_rt_)
      dataframe = pd.DataFrame(data)
      df = dataframe.loc[:, rt_per_service[service]]
      # df = df.interpolate(method ='linear', limit_direction ='both')
      df = df.fillna(method='ffill')
      df = df.fillna(method='bfill')
      for col in df.columns:
        if col.split('_')[-1] == 'sum':
          df[col] = df[col].diff()
          df[col].loc[df[col] < 0] = 0
      df = df.drop([0,1,2],axis=0)


    except:
      print('error1',path_rt_)
      df = pd.DataFrame(5000, index=range(size), columns=cols)
    dfs_rt[service] = df


  rt = []
  for i in containers:
    try:
      dfs_rt[i]['sum'] = dfs_rt[i].sum(axis=1)/len(dfs_rt[i].columns)
      # rt.append(torch.tensor(dfs_rt[i]['sum'].values.tolist())[:size])

      sum = dfs_rt[i]['sum']
      # ma = sum.rolling(window=24,min_periods=1).mean()
      # q = pd.DataFrame(sum)
      # q['ma']=ma

      ma = sum.rolling(window=24,min_periods=1).mean()
      q = pd.DataFrame(sum)
      q['ma']= q['sum'] - ma

      ma20 = sum.rolling(window=24*10,min_periods=1).mean()
      q['ma20']= q['sum'] - ma20

      rt.append(torch.tensor(q.values.tolist())[:size])
    except Exception as e:
      print('error: sum',e)
      rt.append(torch.zeros(size,3))

  data_rt = torch.stack(rt)
  # data_rt = data_rt.unsqueeze(2)

  data_cad = torch.stack(t)


  data = torch.cat((data_cad,data_rt),2)
  return data.transpose(0,1)

services = constants.services
cumulative_cols = constants.cumulative_cols
containers = constants.containers
metrics = constants.metrics
cols = constants.cols
anomalies = constants.anomalies

rt_per_service = dict()
for i in containers:
    rt_per_service[i] = []
for metric in metrics:
    callee = metric.split('_')[3]
    if callee=='PDO': callee='mysql'
    if metric.split('_')[-1] == 'sum':
      rt_per_service[callee].append(metric)

# get train data mean and standard deviation

mean_train = pd.read_csv("norm_data_statistics/mean.csv")
mean_train.pop(mean_train.columns[0])
# print(mean_train.pop(mean_train.columns[0]).head)
std_train = pd.read_csv("norm_data_statistics/std_d.csv")
std_train.pop(std_train.columns[0])

m = torch.tensor(mean_train.values) # mean
s = torch.tensor(std_train.values) # standard deviation

#load normal data
norm_data_tensor = get_data("normal_data/cAdvisor/", "normal_data/response_times/",100000)
#scale normal data
norm_data_tensor = norm_data_tensor - m
norm_data_tensor = norm_data_tensor / s


seqs = 1000//24
st = 0
anom_data = []
for x in anomalies:
  anom_data_instance = get_data('anomaly_data/cAdvisor/','anomaly_data/response_times/',seqs*24,x)

  anom_data_instance = anom_data_instance - m
  anom_data_instance = anom_data_instance / s
  anom_data_instance = anom_data_instance[st:st+seqs*24]
  anom_data_instance = anom_data_instance.reshape(-1,24,12,22)
  anom_data.append(anom_data_instance)
anomaly_data_tensor = torch.stack(anom_data)
print("norm data shape",norm_data_tensor.shape)
print("number of anomalies : ",len(anomalies))
print("anomaly_data_tensor shape",anomaly_data_tensor.shape)
