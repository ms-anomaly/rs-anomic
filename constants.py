
services = ['payment', 'shipping', 'redis', 'mongodb', 'dispatch', 'rabbitmq', 'user', 'mysql', 'catalogue', 'ratings', 'web', 'cart']
anomalies = ['rt-delay-catalogue',
 'packetloss-user',
 'low-bandwidth-user',
 'high-cpu-dispatch',
 'high-latency-user-2',
 'high-load-1500',
 'out-of-order-packets-user-2',
 'high-latency-user',
 'service-down-payment',
 'out-of-order-packets-user',
 'packetloss-user-2',
 'high-fileIO-payment',
 'memory-leak-cart',
  'low-bandwidth-user-2']


cumulative_cols = ['container_cpu_system_seconds_total',
'container_cpu_usage_seconds_total',
'container_cpu_user_seconds_total',
'container_network_receive_bytes_total',
'container_network_receive_errors_total',
'container_network_receive_packets_dropped_total',
'container_network_receive_packets_total',
'container_network_transmit_bytes_total',
'container_network_transmit_errors_total'	,
'container_network_transmit_packets_dropped_total',
'container_network_transmit_packets_total',
'container_fs_io_time_seconds_total',
'container_memory_failures_total',
'container_memory_failcnt',
'container_fs_write_seconds_total']

other_cols = ['container_fs_usage_bytes',
'container_memory_rss',
'container_memory_usage_bytes',
'container_memory_working_set_bytes']

cols = other_cols + cumulative_cols

containers = ['payment', 'shipping', 'redis', 'mongo', 'dispatch', 'rabbitmq', 'user', 'mysql', 'catalogue', 'ratings', 'web', 'cart']
metrics = ['rt_ratings_put_PDO_count', 'rt_ratings_put_PDO_sum', 'rt_payment_delete_cart_count', 'rt_payment_delete_cart_sum', 'rt_cart_get_catalogue_count', 'rt_cart_get_catalogue_sum', 'rt_ratings_get_catalogue_count', 'rt_ratings_get_catalogue_sum', 'rt_catalogue_get_mongo_categories_count', 'rt_catalogue_get_mongo_categories_sum', 'rt_catalogue_get_mongo_products_count', 'rt_catalogue_get_mongo_products_sum', 'rt_catalogue_get_mongo_productscat_count', 'rt_catalogue_get_mongo_productscat_sum', 'rt_catalogue_get_mongo_productsku_count', 'rt_catalogue_get_mongo_productsku_sum', 'rt_catalogue_get_mongo_search_count', 'rt_catalogue_get_mongo_search_sum', 'rt_user_get_mongo_checkid_count', 'rt_user_get_mongo_checkid_sum', 'rt_user_get_mongo_history_count', 'rt_user_get_mongo_history_sum', 'rt_user_get_mongo_users_count', 'rt_user_get_mongo_users_sum', 'rt_user_post_mongo_login_count', 'rt_user_post_mongo_login_sum', 'rt_user_post_mongo_order_count', 'rt_user_post_mongo_order_sum', 'rt_user_post_mongo_register_count', 'rt_user_post_mongo_register_sum', 'rt_web_post_payment_count', 'rt_web_post_payment_sum', 'rt_dispatch_get_rabbitmq_count', 'rt_dispatch_get_rabbitmq_sum', 'rt_web_get_ratings_count', 'rt_web_get_ratings_sum', 'rt_cart_delete_redis_count', 'rt_cart_delete_redis_sum', 'rt_cart_get_redis_count', 'rt_cart_get_redis_sum', 'rt_cart_post_redis_count', 'rt_cart_post_redis_sum', 'rt_user_get_redis_count', 'rt_user_get_redis_sum', 'rt_web_get_shipping_calcid_seconds_count', 'rt_web_get_shipping_calcid_seconds_sum', 'rt_web_get_shipping_code_seconds_count', 'rt_web_get_shipping_code_seconds_sum', 'rt_web_get_shipping_postconfirm_seconds_count', 'rt_web_get_shipping_postconfirm_seconds_sum', 'rt_payment_get_user_count', 'rt_payment_get_user_sum', 'rt_payment_post_user_count', 'rt_payment_post_user_sum']
