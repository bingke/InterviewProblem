# -*- encoding: utf-8 -*-
import pandas as pd
import numpy as np
import cPickle as pickle

# #read product
# print 'read product'
# product_data = pd.read_csv("I:\puzzle1\product.csv.gz", compression='gzip')
# # product_data = raw_data[raw_data.type == 'PARENT']
# product_data[product_data.productCategoryIds.isnull()]
# product_data = product_data[product_data.productCategoryIds.notnull()]
#
# product_data.index = range(len(product_data))
# for indexs in range(len(product_data)):
#     product_data.loc[indexs, ('productCategoryIds')] = (product_data['productCategoryIds'][indexs].split("['")[1]).split("']")[0]
#     product_data.loc[indexs, ('productCategoryIds')] = product_data['productCategoryIds'][indexs].split("',")[0]
# product_data = product_data[['productSku', 'productCategoryIds']]
#
#
# #Combine any two of the types.
# print 'Combine any two of the types'
#
# category_set = set(product_data.productCategoryIds)
# category_list = list(category_set)
# category_list_two = list()
# for i in range(len(category_list)):
#     for j in range(len(category_list)):
#         if i < j:
#             category_list_two.append([category_list[i], category_list[j]])
#
# category_df_two = pd.DataFrame(category_list_two, columns=['category_1', 'category_2'])
# category_df_two.index = range(len(category_df_two))
# category_df_two['distance'] = 0.0
#
# #read product_distance
# print 'read product_distance'
# distance_data = pd.read_csv("I:\puzzle1\product_distance_prod.csv")
# distance_data = distance_data[((distance_data['sku_1'].isin(product_data.productSku)) & (
#     distance_data['sku_2'].isin(product_data.productSku)))]
# distance_data.index = range(len(distance_data))
#
# #Calculating distance
# print 'Calculating distance'
#
# for indexs in range(len(category_df_two)):
#
#     product_sku_1 = product_data[product_data['productCategoryIds'] == category_df_two['category_1'][indexs]]
#     product_sku_2 = product_data[product_data['productCategoryIds'] == category_df_two['category_2'][indexs]]
#     product_set_sku = set(product_sku_1.productSku) | set(product_sku_2.productSku)
#
#     count = 0
#     distance = 0.0
#     for i in range(len(distance_data)):
#         if distance_data['sku_1'][i] in product_set_sku and distance_data['sku_2'][i] in product_set_sku:
#             count += 1
#             distance = distance_data['distance'][i]+distance
#     if(count == 0):
#         category_df_two['distance'][indexs] = 0
#     else:
#         category_df_two['distance'][indexs] = distance/count
#     print indexs
#
# category_df_two.to_csv('category_distance.csv', index=False)
#
#数字-category映射字典
category = pd.read_csv("I:\puzzle1\category.csv.gz", compression='gzip')

id_to_catename = {}
for index in range(len(category)):
    key = category['categoryId'].iloc[index]
    values = str(category['categoryName'].iloc[index])
    id_to_catename[key] = values


#写一个字典用于存最大值
category_df_two = pd.read_csv('category_distance.csv',dtype='str')

sort_distance = {}
for index in range(len(category_df_two)):

    category = str(category_df_two['category_1'].iloc[index])

    if(category in set(category_df_two['category_1'])) and (category in set(category_df_two['category_2'])):
        data1 = category_df_two[category_df_two['category_1'] == category]
        data2 = category_df_two[category_df_two['category_2'] == category]
        print 'one'
        data = pd.concat([data1, data2])

    elif(category in set(category_df_two['category_1'])) :
        data = category_df_two[category_df_two['category_1'] == category]
        print 'two'

    elif(category in set(category_df_two['category_2'])):
        data = category_df_two[category_df_two['category_2'] == category]
        print 'three'

    data = data.sort_values(by='distance', ascending=False)
    if (len(data > 4)):
        data = data[:4]

    if category in id_to_catename.keys():
        categoryname = id_to_catename[category]

    similar = pd.concat([data['category_1'], data['category_2']])
    similar = set(similar)
    similar.remove(category)
    similar_list = list(similar)


    for i in range(len(similar_list)):
        if similar_list[i] in id_to_catename.keys():
            similar_list[i] = id_to_catename[similar_list[i]]

    sort_distance[categoryname] = similar_list

# f = open('I:\puzzle1\sort_distance.pkl', 'wb')
# pickle.dump(sort_distance, f)

#读入pickle转换成表
sort_list_distance = list()

for key,values in sort_distance.items():
    values.insert(0,key)
    sort_list_distance.append(values)
    print values
sort_df_distance = pd.DataFrame(sort_list_distance)
sort_df_distance.columns = [['category', 'simliary_1', 'simliary_2','simliary_3','simliary_4']]
sort_df_distance.to_csv('sort_distance.csv',index=False)

print 'a'