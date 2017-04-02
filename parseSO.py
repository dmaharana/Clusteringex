#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 14:01:48 2017

@author: titu
"""
from lxml import etree
import csv
from dateutil import parser as dateparser
import re

# regegx to find code snippets
code_match = re.compile('<pre>(.*?)</pre>', re.MULTILINE | re.DOTALL)
link_match = re.compile(
    '<a href="http://.*?".*?>(.*?)</a>', re.MULTILINE | re.DOTALL)
img_match = re.compile('<img(.*?)/>', re.MULTILINE | re.DOTALL)
tag_match = re.compile('<[^>]*>', re.MULTILINE | re.DOTALL)

def filter_html(s):
    num_code_lines = 0
    link_count_in_code = 0
    code_free_s = s

    num_images = len(img_match.findall(s))

    # remove source code and count how many lines
    for match_str in code_match.findall(s):
        num_code_lines += match_str.count('\n')
        code_free_s = code_match.sub("", code_free_s)

        # sometimes source code contain links, which we don't want to count
        link_count_in_code += len(link_match.findall(match_str))

    links = link_match.findall(s)
    link_count = len(links)

    link_count -= link_count_in_code

    link_free_s = re.sub(
        " +", " ", tag_match.sub('', code_free_s)).replace("\n", "")

    for link in links:
        if link.lower().startswith("http://"):
            link_free_s = link_free_s.replace(link, '')

    num_text_tokens = link_free_s.count(" ")

    return link_free_s, num_text_tokens, num_code_lines, link_count, num_images

def parse_so_xml(xmlfile):
    csvHeader = 'Id,ParentId,IsAccepted,TimeToAnswer,Score,Text,NumTextTokens,NumCodeLines,LinkCount,NumImages'.split(',')

    tree = etree.parse(xmlfile)

    rows = [it for it in tree.findall('row')]
    csvData = []
    rowIdListId = {}
    noQuestions = 0
    noAnswers = 0

    #isAccFlg = False

    for row in rows:
        rowId = row.get('Id')
        parentId = row.get('ParentId')
        score = row.get('Score')
        Text, NumTextTokens, NumCodeLines, LinkCount, NumImages = filter_html(
                    row.get('Body'))
        timeToAns = 'NA'
        isAccepted = 'NA'
        creationDate = row.get('CreationDate')

        entryType = row.get('PostTypeId')
        if entryType == '1':
           noQuestions += 1
           parentId = -1
           acceptedAns = row.get('AcceptedAnswerId')
           if acceptedAns:
              questionCreatedDate = dateparser.parse(creationDate)
              rowIdListId[rowId] = [acceptedAns, len(csvData), questionCreatedDate]

        elif entryType == '2':
             noAnswers += 1
             isAccepted = 0
             if parentId in rowIdListId and rowIdListId[parentId][0] == rowId:
                questionCreatedDate = rowIdListId[parentId][2]
                answerDate = dateparser.parse(creationDate)
                timeToAns = (answerDate - questionCreatedDate).seconds
                csvData[rowIdListId[parentId][1]][csvHeader.index('TimeToAnswer')] = timeToAns
                isAccepted = 1
                #isAccFlg = True
                #print('Solution accepted: {}'.format(rowId))
        else:
            continue

        csvRow = [rowId, parentId, isAccepted, timeToAns, score, Text, NumTextTokens, NumCodeLines, LinkCount, NumImages]
        csvData.append(csvRow)
        '''
        if isAccFlg:
           print(csvRow)
           print(csvData[rowIdListId[parentId][1]])
           isAccFlg = False

    #print(rowIdListId)
    '''
    if len(csvData[0]) > 0:
        csvData.insert(0, csvHeader)
    print('Q: {}, A: {}'.format(noQuestions, noAnswers))

    return csvData

def write2csv(csvFile, csvData):
    with open(csvFile, 'w') as fh:
         csvWriter = csv.writer(fh)
         csvWriter.writerows(csvData)
         print('OutputFile: {}'.format(csvFile))

def main():
    xmlfile = '/home/titu/Documents/pyworkspace/Clusteringex/iot.stackexchange.com/Posts.xml'
    outfile = '/home/titu/Documents/pyworkspace/Clusteringex/soxml.csv'

    csvdata = parse_so_xml(xmlfile)
    write2csv(outfile, csvdata)

if __name__ == "main":
    print('Calling main')
    main()
main()

