import json

'''
with open('./json_sample.json', 'r', encoding='UTF-8') as json_f:
    json_f_dict = json.load(json_f)
'''


class Resolve:

    def __init__(self, f_name):
        self.f_name = f_name

    def resolve_json(self):

        with open(self.f_name, 'r', encoding='UTF-8') as json_f:
            json_f_dict = json.load(json_f)
            #data filed is for json recived from web page directly
            #data_dict = json_f_dict['data']
            data_dict = json_f_dict

        return data_dict['part_info']

    def resolve_item(self):
        data = self.resolve_json()

        item_list = []
        for item in data:
            if 'subject_list' in item.keys():
                for sub_question in item['subject_list']:
                    item_list.append(sub_question['pos_list'])
            else:
                continue
        return item_list

    def resolve_part(self):
        data = self.resolve_json()
        part_list = []
        for item in data:
            part_list.append(item['pos_list'])
        return part_list


if __name__ == '__main__':
    #file_path = './json_sample.json'
    file_path = './recive.json'
    resovle_value = Resolve(file_path)

    item = resovle_value.resolve_item()
    part = resovle_value.resolve_part()

    print(len(item))
    for i in part:
        print(i)
