#import alignment
#import os
#import sys
import csv

#MED = alignment.MinEditDistance()


def GetParadigmsVariables(linelist):
    """
    Read in the paradigm file;
    Put all paradigms into a list: paradigms_list
    Put all variables corresponding to each paradigm into another list: variables_list
    Make a list of variables without identical elements: variable_list
    Renumber the variables: variable_id_dict
    Keep track of the correspondence between the new id and each variable: id_variable_dict
    """

    paradigms_list = []
    paradigm = []
    variable_list = []
    variables_list = []
    for line in linelist:
        if '\t' in line:
            ps, vs = line.strip().split('\t')
            ps = ps.strip().split('#')
            paradigms = [x.strip().split(':')[0] for x in ps]
            paradigms_list.append(paradigms)

            # print (vs)
            vs = vs.strip().split('#')
            for v in vs:
                v = v.strip().split(',')
                variables = [x.strip().split('=')[1] for x in v if '=' in x]
                variables_list.append(variables)
                for nv in v:
                    n, va = nv.strip().split('=')
                    if va not in variable_list:
                        variable_list.append(va)
        else:
            paradigms = [x.strip().split(':')[0] for x in line.strip().split('#')]
            paradigms_list.append(paradigms)
    variable_id_dict = {v: str(i + 1) for i, v in enumerate(variable_list)}
    id_variable_dict = {v: k for k, v in variable_id_dict.items()}

    return paradigms_list, variables_list, variable_id_dict, id_variable_dict


def NewParadigms(paradigms_list, variables_list, variable_id_dict, id_variable_dict):
    """
    Rewrite the paradigms with new variable ids.
    The output is still a list of paradigm-lists as the old one.
    """

    new_paradigms_list = []
    for ps, vs in zip(paradigms_list, variables_list):
        v_id_dict = {str(i + 1): variable_id_dict[v] for i, v in enumerate(vs)}
        new_ps_list = []
        for p in ps:
            p = p.split('+')
            new_p_list = []
            for item in p:
                if item in v_id_dict:
                    item = v_id_dict[item]
                new_p_list.append(item)
            new_p = '+'.join(x for x in new_p_list)
            new_ps_list.append(new_p)
        new_paradigms_list.append(new_ps_list)
    return new_paradigms_list


def GeneralizeP(tp_dict_list):
    """
    Takes as input all the paradigms for each POS
    Re-expresses such paradigms with y+num, and group the ones with the same structure after re-expression.
    It also record what are the ys.
    """
    tags = list(tp_dict_list[0].keys())
    #print(tags)

    tag_join = '#'.join(x for x in tags)
    paradigm_join_list = []

    tpv_dict_list = []
    all_paradigm_variable_list = []

    vy_dict_list = []

    for tp_dict in tp_dict_list:
        #print(tp_dict)
        variable_dict = {}
        vc = 0  # vc is the count of the variable that changes between slots in the paradigm
        # for example:
        # run ran
        # 1+u+2 1+a+2
        # vc counts things like "u" and "a"
        paradigms = [tp_dict[t] for t in tags]  # one paradigm line in fixed order
        # print ('#'.join(x for x in paradigms), '\n')
        paradigm_variable_list = []
        for item in paradigms:
            # print (item)
            items = item.strip().split('+')
            for it in items:
                if it.isdigit() == False:
                    if it not in variable_dict:
                        vc += 1
                        variable_dict[it] = 'y' + str(vc)  # it records with varaible corresponds to which y

            ##This part cannot be merged with the previous loop,
            ##Because need the variable_dict which is generated in the previous loop.
            ##This step is to replace that part that changes between slots with variables of y+num
            it_variable_list = []
            for it in items:
                if it.isdigit():
                    it_variable_list.append(it)
                else:
                    it_variable_list.append(variable_dict[it])

            it_variable = '+'.join(x for x in it_variable_list)  # reexpress each slot in the paradigm

            paradigm_variable_list.append(it_variable)
            # paradigm_variable_list is basically the same as paradigms
            # the differences are the parts which changes between slots in paradigms are reexpressed with y+num in paradigm_variable_list
        all_paradigm_variable_list.append(paradigm_variable_list)
        # all_paradigms_variable_list contains the same thing as tp_dict_list
        # but it is a list of paradigms re-expressed with y+num
        # print ()
        vc = 0
        vy_dict_list.append(
            {v: k for k, v in variable_dict.items()})  # it records which y corresponds to which varaible

    # print ("* * * * * * * * * * \n")

    # change list of lists, to list of strings
    tpv_str_list = []
    for paradigm_variable_list in all_paradigm_variable_list:
        tpv_str_list.append('#'.join(x for x in paradigm_variable_list))

    # put paradigms of the same struture after reexpressed with y+num into dictionary varaible_paradigm_dict: {paradigm1_reexpressed_with_ys:[p1_with_this_structure, p2_with_this_structure, ... ], ...}
    variable_paradigm_dict = {}
    for item in set(tpv_str_list):
        for tpv_str, tp_dict in zip(tpv_str_list, tp_dict_list):
            inflections = '#'.join(x for x in [tp_dict[t] for t in tags])
            if tpv_str == item:
                if item not in variable_paradigm_dict.keys():
                    variable_paradigm_dict[item] = [inflections]
                else:
                    variable_paradigm_dict[item].append(inflections)

    return vy_dict_list, all_paradigm_variable_list, tags, variable_paradigm_dict


def POSparadigms(fp):
    """
    Read in a paradigm file,
    Put the paradigms for different POS into different lists
    """

    alltp_dict_list = []
    ntp_dict_list = []
    adjtp_dict_list = []
    vtp_dict_list = []
    for l in fp:
        tp_dict = {}
        line = l.strip().split('\t')
        inflections = line[0].strip().split('#')
        for item in inflections:
            # print (item)
            p, t = item.strip().split(':')
            tp_dict[t] = p
        alltp_dict_list.append(tp_dict)
        #if ':pos=noun,' in l or ':pos=nounadj,' in l or 'TAG=N,TAG=LEMMA' in l:
        if ':pos=noun,' in l or ':pos=nounadj,' in l or 'TAG=N,TAG=LEMMA' in l:
            ntp_dict_list.append(tp_dict)
        #if 'TAG=ADJ,TAG=LEMMA' in l:
        if 'TAG=ADJ,TAG=LEMMA' in l:
            adjtp_dict_list.append(tp_dict)
        #if ':pos=verb,' in l or 'TAG=V,TAG=LEMMA' in l:
        if ':pos=verb,' in l or 'TAG=V,TAG=LEMMA'in l:
            vtp_dict_list.append(tp_dict)
    return ntp_dict_list, adjtp_dict_list, vtp_dict_list, alltp_dict_list

def ParadigmCounts(languagelist, ppath, csvname):
    """
    Loop over the langauges in the language list;
    For each language:
        Read in the file of 1st-order paradigms in the ppath;
        Print out the counts of 1st-order and 2nd-order paradigms for each part of speech;
    Also output the count information of every language into a csv file.
    """


    csvhead = ['Language', 'N-1stOrder', 'N-2ndOrder', 'V-1stOrder', 'V-2ndOrder', 'ADJ-1stOrder', 'ADJ-2ndOrder',
               'Total-1stOrder', 'Total-2ndOrder']
    csvvalues = {'Language': ['Language'], 'N-1stOrder': ['N-1stOrder'], 'N-2ndOrder': ['N-2ndOrder'],
                 'V-1stOrder': ['V-1stOrder'], 'V-2ndOrder': ['V-2ndOrder'],
                 'ADJ-1stOrder': ['ADJ-1stOrder'], 'ADJ-2ndOrder': ['ADJ-2ndOrder'],
                 'Total-1stOrder': ['Total-1stOrder'], 'Total-2ndOrder': ['Total-2ndOrder']}

    for language in languagelist:

        print(language)
        csvvalues['Language'].append(language)
        for item in csvhead[1:]:
            csvvalues[item].append(0)

        paradigmfile = open(ppath + language + '.p')
        ntp_dict_list, adjtp_dict_list, vtp_dict_list, alltp_dict_list = POSparadigms(paradigmfile)

        paranum = len(ntp_dict_list) + len(vtp_dict_list) + len(adjtp_dict_list)

        yparanum = 0
        if len(ntp_dict_list) != 0:
            pos = 'n'
            vy_dict_list, _, tags, variable_paradigm_dict = GeneralizeP(ntp_dict_list)
            yparanum += len(variable_paradigm_dict)
            print('# of paradigms for %s: %d' % (pos, len(ntp_dict_list)))
            print('# of paradigms for %s after y-replacement: %d' % (pos, len(variable_paradigm_dict)))
            csvvalues['N-1stOrder'][-1] = len(ntp_dict_list)
            csvvalues['N-2ndOrder'][-1] = len(variable_paradigm_dict)
            # paradigm_structures = FileRegroup(language, pos, tags, variable_paradigm_dict, paligned)


        if len(adjtp_dict_list) != 0:
            pos = 'adj'
            vy_dict_list, _, tags, variable_paradigm_dict = GeneralizeP(adjtp_dict_list)
            yparanum += len(variable_paradigm_dict)
            print('# of paradigms for %s: %d' % (pos, len(adjtp_dict_list)))
            print('# of paradigms for %s after y-replacement: %d' % (pos, len(variable_paradigm_dict)))
            csvvalues['ADJ-1stOrder'][-1] = len(adjtp_dict_list)
            csvvalues['ADJ-2ndOrder'][-1] = len(variable_paradigm_dict)
            # paradigm_structures = FileRegroup(language, pos, tags, variable_paradigm_dict, paligned)

        if len(vtp_dict_list) != 0:
            pos = 'v'
            vy_dict_list, _, tags, variable_paradigm_dict = GeneralizeP(vtp_dict_list)
            yparanum += len(variable_paradigm_dict)
            print('# of paradigms for %s: %d' % (pos, len(vtp_dict_list)))
            print('# of paradigms for %s after y-replacement: %d' % (pos, len(variable_paradigm_dict)))
            csvvalues['V-1stOrder'][-1] = len(vtp_dict_list)
            csvvalues['V-2ndOrder'][-1] = len(variable_paradigm_dict)
            # paradigm_structures = FileRegroup(language, pos, tags, variable_paradigm_dict, paligned)

        print('--------------')
        print('# of paradigms for all POS: ', paranum)
        print('# of paradigms for all POS after y-replacement: ', yparanum)
        csvvalues['Total-1stOrder'][-1] = paranum
        csvvalues['Total-2ndOrder'][-1] = yparanum

    csvoutput = list(zip(csvvalues['Language'],
                         csvvalues['N-1stOrder'], csvvalues['N-2ndOrder'],
                         csvvalues['V-1stOrder'], csvvalues['V-2ndOrder'],
                         csvvalues['ADJ-1stOrder'], csvvalues['ADJ-2ndOrder'],
                         csvvalues['Total-1stOrder'], csvvalues['Total-2ndOrder']))
    #print(csvoutput)

    with open(csvname, 'w') as fcsv:
        fw = csv.writer(fcsv, delimiter=',')
        fw.writerows(csvoutput)

