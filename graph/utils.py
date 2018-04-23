from django.db.models import Count, Sum, Avg

from problem.models import Problem


def _x_number(field, name, unit, num):
    return {
        'chart_type': 'x-number',
        'zoom': 0,
        'columns': [
            {
                'type': 'y',
                'field': field,
                'name': name,
                'unit': unit
            }
        ],
        'rows': [
            {
                field: num
            }
        ]
    }


def _x_pie(x_field, x_name, y_field, y_name, rows):
    return {
        "chart_type": "x-pie",
        "zoom": 0,
        "columns": [
            {
                "type": "x",
                "field": x_field,
                "name": x_name
            },
            {
                "type": "y",
                "field": y_field,
                "name": y_name
            }
        ],
        "rows": rows
    }


def _x_line_area(x_field, x_name, y_field, y_name, rows):
    return {
        "chart_type": "x-line-area",
        "zoom": 0,
        "columns": [
            {
                "type": "x",
                "field": x_field,
                "name": x_name
            },
            {
                "type": "y",
                "field": y_field,
                "name": y_name
            }
        ],
        "rows": rows
    }


def _x_bar(x_field, x_name, y_field, y_name, rows):
    return {
        "chart_type": "x-bar",
        "zoom": 0,
        "columns": [
            {
                "type": "x",
                "field": x_field,
                "name": x_name,
            },
            {
                "type": "y",
                "field": y_field,
                "name": y_name
            }
        ],
        "rows": rows
    }


def slice_1(queryset, fl):
    # 问题类别数量
    p_clf_count = queryset.values(
        'classification__name').annotate(Count('classification')).count()
    return _x_number(fl.y_field, fl.y_name, fl.y_unit, p_clf_count)


def slice_2(queryset, fl):
    # 问题类别占比
    x_pie_list = []
    p_clf_list = queryset.values(
        'classification__name').annotate(p_count=Count('classification'))
    for clf in p_clf_list:
        if clf['classification__name']:
            x_pie_list.append({
                fl.x_field: clf['classification__name'],
                fl.y_field: clf['p_count']
            })

    return _x_pie(fl.x_field, fl.x_name, fl.y_field, fl.y_name, x_pie_list)


def slice_3(queryset, fl):
    # 各类问题发生走势
    x_line_area_list = []
    p_line_area_list = queryset.values(
        'start_time', 'classification_id', 'classification__name').annotate(
        p_count=Count('id')).order_by(
        'start_time', 'classification_id')

    res_dict = {
        "chart_type": "x-line-area",
        "zoom": 0,
        "columns": [
            {
                "type": "x",
                "field": fl.x_field,
                "name": fl.x_name
            }
        ],
        "rows": [],
    }

    classifications = {i['classification_id']: i['classification__name']
                       for i in p_line_area_list}

    column_list = []
    for k, v in classifications.items():
        column_list.append({
            "type": "y",
            "field": '{}_{}'.format(fl.y_field, k),
            "name": v,
            'unit': fl.y_name,
        })

    res_dict['columns'].extend(column_list)

    item_dict = {}
    for i in p_line_area_list:
        for v in classifications.keys():
            if item_dict.get(i['start_time'], None):
                item_dict[i['start_time']]['{}_{}'.format(fl.y_field, v)] = item_dict[i['start_time']].get('{}_{}'.format(fl.y_field, v), 0) + (i['p_count'] if i['classification_id'] == v else 0)
            else:
                item_dict[i['start_time']] = {
                    '{}_{}'.format(fl.y_field, v): i['p_count'] if i['classification_id'] == v else 0
                }

    for k, v in item_dict.items():
        tmp_dict = {
            fl.x_field: k
        }
        for a, b in v.items():
            tmp_dict[a] = b

        x_line_area_list.append(tmp_dict)

    res_dict['rows'] = x_line_area_list

    return res_dict


def slice_4(queryset, fl):
    # 问题总数
    p_total_count = queryset.count()
    return _x_number(fl.y_field, fl.y_name, fl.y_unit, p_total_count)


def slice_5(queryset, fl):
    # 问题总数量发生走势
    x_line_area_list = []
    p_line_area_list = queryset.values(
        'start_time').annotate(
        p_count=Count('classification')).order_by('start_time')

    for clf in p_line_area_list:
        x_line_area_list.append({
            fl.x_field: clf['start_time'].strftime('%Y-%m-%d'),
            fl.y_field: clf['p_count']
        })

    return _x_line_area(fl.x_field, fl.x_name, fl.y_field, fl.y_name,
                        x_line_area_list)


def slice_6(queryset, fl):
    # 问题处理耗时排行
    x_bar_list = []
    p_bar_list = queryset.filter(process_time__gt=0).values(
        'jira_code', 'process_time').order_by('process_time')

    for i in p_bar_list:
        x_bar_list.append({
            fl.x_field: i['jira_code'],
            fl.y_field: i['process_time']
        })

    return _x_bar(fl.x_field, fl.x_name, fl.y_field, fl.y_name, x_bar_list)


def slice_7(queryset, fl):
    # 问题类别处理耗时排行
    x_bar_list = []
    p_bar_list = queryset.filter(process_time__gt=0).values(
        'classification__name').annotate(
        pro_sum=Sum('process_time')).order_by('pro_sum')

    for i in p_bar_list:
        x_bar_list.append({
            fl.x_field: i['classification__name'],
            fl.y_field: i['pro_sum']
        })

    return _x_bar(fl.x_field, fl.x_name, fl.y_field, fl.y_name, x_bar_list)


# ------------------------问题模块---------------------
def slice_8(queryset, fl):
    # 各模块故障率
    x_pie_list = []
    p_clf_list = queryset.values(
        'modules__name', 'modules__platform__name'
    ).annotate(p_count=Count('modules'))

    for clf in p_clf_list:
        if clf['modules__name']:  # 解决manytomany时不关联的记录
            x_pie_list.append({
                fl.x_field: '{}/{}'.format(clf['modules__name'],
                                           clf['modules__platform__name']),
                fl.y_field: clf['p_count']
            })

    return _x_pie(fl.x_field, fl.x_name, fl.y_field, fl.y_name, x_pie_list)


def slice_9(queryset, fl):
    # 各模块问题发生走势
    x_line_area_list = []
    p_line_area_list = queryset.values(
        'start_time', 'modules', 'modules__name', 'modules__platform__name'
    ).annotate(p_count=Count('id')).order_by('start_time', 'modules')

    res_dict = {
        "chart_type": "x-line-area",
        "zoom": 0,
        "columns": [
            {
                "type": "x",
                "field": fl.x_field,
                "name": fl.x_name
            }
        ],
        "rows": [],
    }

    classifications = {i['modules']: '{}/{}'.format(
        i['modules__name'], i['modules__platform__name'])
        for i in p_line_area_list}

    column_list = []
    for k, v in classifications.items():
        column_list.append({
            "type": "y",
            "field": '{}_{}'.format(fl.y_field, k),
            'name': v,
            "unit": fl.y_name
        })

    res_dict['columns'].extend(column_list)

    item_dict = {}
    for i in p_line_area_list:
        for v in classifications.keys():
            if item_dict.get(i['start_time'], None):
                item_dict[i['start_time']]['{}_{}'.format(fl.y_field, v)] = item_dict[i['start_time']].get('{}_{}'.format(fl.y_field, v), 0) + (i['p_count'] if i['modules'] == v else 0)
            else:
                item_dict[i['start_time']] = {
                    '{}_{}'.format(fl.y_field, v): i['p_count'] if i['modules'] == v else 0
                }

    for k, v in item_dict.items():
        tmp_dict = {
            fl.x_field: k
        }
        for a, b in v.items():
            tmp_dict[a] = b

        x_line_area_list.append(tmp_dict)

    res_dict['rows'] = x_line_area_list

    return res_dict


def slice_10(queryset, fl):
    # 各模块故障数量排行
    x_bar_list = []
    p_bar_list = queryset.values(
        'modules__name', 'modules__platform__name').annotate(
        p_count=Count('id')).order_by('p_count')

    for i in p_bar_list:
        x_bar_list.append({
            fl.x_field: '{}/{}'.format(i['modules__name'],
                                       i['modules__platform__name']),
            fl.y_field: i['p_count'],
        })

    return _x_bar(fl.x_field, fl.x_name, fl.y_field, fl.y_name, x_bar_list)


def slice_11(queryset, fl):
    # 各模块故障种类多样性排行
    x_bar_list = []
    p_bar_list = queryset.values(
        'modules', 'modules__name', 'modules__platform__name', 'classification'
    ).annotate(p_count=Count('classification')).order_by('modules')

    tmp_dict = {}
    for i in p_bar_list:
        module_platform = '{}/{}'.format(i['modules__name'],
                                         i['modules__platform__name'])
        if tmp_dict.get(module_platform, None):
            tmp_dict[module_platform].add(i['classification'])
        else:
            tmp_dict[module_platform] = {i['classification']}

    for k, v in tmp_dict.items():
        x_bar_list.append({
            fl.x_field: k,
            fl.y_field: len(v),
        })

    x_bar_list = sorted(x_bar_list, key=lambda x: x[fl.y_field])

    return _x_bar(fl.x_field, fl.x_name, fl.y_field, fl.y_name, x_bar_list)


def slice_12(queryset, fl):
    # 各模块故障修复率排行
    x_bar_list = []
    p_bar_list = queryset.filter(process_time__gt=0).values(
        'modules', 'modules__name', 'modules__platform__name'
    ).annotate(p_count=Count('modules'))

    p_bar_list2 = queryset.values(
        'modules', 'modules__name', 'modules__platform__name'
    ).annotate(p_count=Count('modules'))

    tmp_dict = {}
    for i in p_bar_list:
        module_platform = '{}/{}'.format(i['modules__name'],
                                         i['modules__platform__name'])
        tmp_dict[module_platform] = i['p_count']

    tmp_dict2 = {}
    for i in p_bar_list2:
        module_platform = '{}/{}'.format(i['modules__name'],
                                         i['modules__platform__name'])
        tmp_dict2[module_platform] = i['p_count']

    tmp_all_dict = {k: round(tmp_dict.get(k, 0) / tmp_dict2.get(k, 1), 4)
                    for k in set(tmp_dict) | set(tmp_dict2)}

    for k, v in tmp_all_dict.items():
        x_bar_list.append({
            fl.x_field: k,
            fl.y_field: v
        })

    x_bar_list = sorted(x_bar_list, key=lambda x: x[fl.y_field])

    return _x_bar(fl.x_field, fl.x_name, fl.y_field, fl.y_name, x_bar_list)


def slice_13(queryset, fl):
    # 各模块修复平均耗时排行
    x_bar_list = []
    p_bar_list = queryset.filter(process_time__gt=0).values(
        'modules', 'modules__name', 'modules__platform__name'
    ).annotate(pro_avg=Avg('process_time'))

    for i in p_bar_list:
        x_bar_list.append({
            fl.x_field: '{}/{}'.format(i['modules__name'],
                                       i['modules__platform__name']),
            fl.y_field: round(i['pro_avg'], 1),
        })

    x_bar_list = sorted(x_bar_list, key=lambda x: x[fl.y_field])

    return _x_bar(fl.x_field, fl.x_name, fl.y_field, fl.y_name, x_bar_list)


def slice_14(queryset, fl):
    # 各模块按照发生故障等级排行
    x_bar_list = []
    p_bar_list = queryset.values(
        'modules', 'modules__name', 'modules__platform__name'
    ).annotate(pro_avg=Avg('level'))

    for i in p_bar_list:
        x_bar_list.append({
            fl.x_field: '{}/{}'.format(i['modules__name'],
                                       i['modules__platform__name']),
            fl.y_field: round(i['pro_avg'], 1),
        })

    x_bar_list = sorted(x_bar_list, key=lambda x: x[fl.y_field])

    return _x_bar(fl.x_field, fl.x_name, fl.y_field, fl.y_name, x_bar_list)


# ------------------------问题平台---------------------
def slice_15(queryset, fl):
    # 各平台故障率
    x_pie_list = []
    p_clf_list = queryset.values(
        'platforms__name').annotate(p_count=Count('platforms'))

    for clf in p_clf_list:
        if clf['platforms__name']:
            x_pie_list.append({
                fl.x_field: clf['platforms__name'],
                fl.y_field: clf['p_count']
            })

    return _x_pie(fl.x_field, fl.x_name, fl.y_field, fl.y_name, x_pie_list)


def slice_16(queryset, fl):
    # 各平台问题发生走势
    x_line_area_list = []
    p_line_area_list = queryset.values(
        'start_time', 'platforms', 'platforms__name').annotate(
        p_count=Count('id')).order_by(
        'start_time', 'platforms')

    res_dict = {
        "chart_type": "x-line-area",
        "zoom": 0,
        "columns": [
            {
                "type": "x",
                "field": fl.x_field,
                "name": fl.x_name
            }
        ],
        "rows": [],
    }

    classifications = {i['platforms']: i['platforms__name']
                       for i in p_line_area_list}

    column_list = []
    for k, v in classifications.items():
        column_list.append({
            "type": "y",
            "field": '{}_{}'.format(fl.y_field, k),
            "name": v,
            "unit": fl.y_name,
        })

    res_dict['columns'].extend(column_list)

    item_dict = {}
    for i in p_line_area_list:
        for v in classifications.keys():
            if item_dict.get(i['start_time'], None):
                item_dict[i['start_time']]['{}_{}'.format(fl.y_field, v)] = item_dict[i['start_time']].get('{}_{}'.format(fl.y_field, v), 0) + (i['p_count'] if i['platforms'] == v else 0)
            else:
                item_dict[i['start_time']] = {
                    '{}_{}'.format(fl.y_field, v): i['p_count'] if i['platforms'] == v else 0
                }

    for k, v in item_dict.items():
        tmp_dict = {
            fl.x_field: k
        }
        for a, b in v.items():
            tmp_dict[a] = b

        x_line_area_list.append(tmp_dict)

    res_dict['rows'] = x_line_area_list

    return res_dict


def slice_17(queryset, fl):
    # 各平台故障数量排行
    x_bar_list = []
    p_bar_list = queryset.values('platforms__name').annotate(
        p_count=Count('id')).order_by('p_count')

    for i in p_bar_list:
        x_bar_list.append({
            fl.x_field: i['platforms__name'],
            fl.y_field: i['p_count'],
        })

    return _x_bar(fl.x_field, fl.x_name, fl.y_field, fl.y_name, x_bar_list)


def slice_18(queryset, fl):
    # 各平台故障种类多样性排行
    x_bar_list = []
    p_bar_list = queryset.values(
        'platforms__name', 'classification'
    ).annotate(p_count=Count('classification')).order_by('platforms')

    tmp_dict = {}
    for i in p_bar_list:
        platform = i['platforms__name']
        if tmp_dict.get(platform, None):
            tmp_dict[platform].add(i['classification'])
        else:
            tmp_dict[platform] = {i['classification']}

    for k, v in tmp_dict.items():
        x_bar_list.append({
            fl.x_field: k,
            fl.y_field: len(v),
        })

    x_bar_list = sorted(x_bar_list, key=lambda x: x[fl.y_field])

    return _x_bar(fl.x_field, fl.x_name, fl.y_field, fl.y_name, x_bar_list)


def slice_19(queryset, fl):
    # 各平台故障修复率排行
    x_bar_list = []
    p_bar_list = queryset.filter(process_time__gt=0).values(
        'platforms__name').annotate(p_count=Count('platforms__name'))

    p_bar_list2 = queryset.values(
        'platforms__name').annotate(p_count=Count('platforms__name'))

    tmp_dict = {}
    for i in p_bar_list:
        tmp_dict[i['platforms__name']] = i['p_count']

    tmp_dict2 = {}
    for i in p_bar_list2:
        tmp_dict2[i['platforms__name']] = i['p_count']

    tmp_all_dict = {k: round(tmp_dict.get(k, 0) / tmp_dict2.get(k, 1), 4)
                    for k in set(tmp_dict) | set(tmp_dict2)}

    for k, v in tmp_all_dict.items():
        x_bar_list.append({
            fl.x_field: k,
            fl.y_field: v
        })

    x_bar_list = sorted(x_bar_list, key=lambda x: x[fl.y_field])

    return _x_bar(fl.x_field, fl.x_name, fl.y_field, fl.y_name, x_bar_list)


def slice_20(queryset, fl):
    # 各模块修复平均耗时排行
    x_bar_list = []
    p_bar_list = queryset.filter(process_time__gt=0).values(
        'platforms__name').annotate(pro_avg=Avg('process_time'))

    for i in p_bar_list:
        x_bar_list.append({
            fl.x_field: i['platforms__name'],
            fl.y_field: round(i['pro_avg'], 1),
        })

    x_bar_list = sorted(x_bar_list, key=lambda x: x[fl.y_field])

    return _x_bar(fl.x_field, fl.x_name, fl.y_field, fl.y_name, x_bar_list)


def slice_21(queryset, fl):
    # 各平台按照发生故障等级排行
    x_bar_list = []
    p_bar_list = queryset.values(
        'platforms__name').annotate(pro_avg=Avg('level'))

    for i in p_bar_list:
        x_bar_list.append({
            fl.x_field: i['platforms__name'],
            fl.y_field: round(i['pro_avg'], 1),
        })

    x_bar_list = sorted(x_bar_list, key=lambda x: x[fl.y_field])

    return _x_bar(fl.x_field, fl.x_name, fl.y_field, fl.y_name, x_bar_list)
