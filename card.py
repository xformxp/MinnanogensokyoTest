#coding: utf8
import plists
import utils
import userinf
import requests
import general

def cardmenu():
    utils.drawline('CARDMENU')
    print '0. 查看人物'
    print '1. 返回'
    return utils.select(1)

def carddetail(cardlist):
    utils.drawline('CARDDETAIL')
    cardid = raw_input("Input card id:")
    if not cardid in plists.get_plist('card'):
        print 'Input error.'
        return
    if not cardid in cardlist:
        print 'You do not possess this card.'
        return
    card = cardlist[cardid]
    print cardid + '\t' + card['cardname'] + ', LV' + card['level'] + ', ' + card['exp'] + '/' + card['upexp']
    print 'Loyalty: ' + card['loyalty'] + ', Points: ' + card['feat']
    print 'Skinid: ' + card['skinid'] + ', ' + plists.get_plist('skin')[card['skinid']]['skinname'] + ', HasSkins: ' + card['haveskinids']
    print 'HP: ' + card['hp'] + ', Def: ' + card['def'] + ', A.rate: ' + card['avoid'] + ', Luck: ' + card['lucky']
    print 'AtkMel: ' + card['atk_mel'] + ', AtkRang: ' + card['atk_rang'] + ', H.rate: ' + card['hitrate'] + ', Crit: ' + card['crit']
    print 'Block: ' + card['block'] + ', Speed: ' + card['speed'] 
    if card['equipment_id_wq'] == '':
        print 'Weapon: None,', 
    else:
        print 'Weapon: ' + card['equipment_id_wq'] + ' ' + plists.get_plist('equipment')[card['equipment_id_wq']]['equipmentname'] + ',',
    if card['equipment_id_fj'] == '':
        print 'Armor: None'
    else:
        print 'Armor: ' + card['equipment_id_fj'] + ' ' + plists.get_plist('equipment')[card['equipment_id_fj']]['equipmentname']
    spell_atk = plists.get_plist('spell')[card['spell_card_id_atk']]
    spell_def = plists.get_plist('spell')[card['spell_card_id_def']]
    spell_aid = plists.get_plist('spell')[card['spell_card_id_aid']]
    print 'Spell Atk: ' + card['spell_card_id_atk'] + ' ' + spell_atk['name'] + spell_atk['spell_point'] + ', NeedLevel: ' + spell_atk['need_level'] + ', ' + spell_atk['spell_rate'] + '%'
    print spell_atk['content']
    print 'Spell Def: ' + card['spell_card_id_def'] + ' ' + spell_def['name'] + spell_def['spell_point'] + ', NeedLevel: ' + spell_def['need_level'] + ', ' + spell_def['spell_rate'] + '%'
    print spell_def['content']
    print 'Spell Aid: ' + card['spell_card_id_aid'] + ' ' + spell_aid['name'] + spell_aid['spell_point'] + ', NeedLevel: ' + spell_aid['need_level'] + ', ' + spell_aid['spell_rate'] + '%'
    print spell_aid['content']
    #TODO
    print 'TODO: 加点，切换装备，咕了'

def cardfunc():
    utils.drawline('CARD')
    cardlist = {}
    for card in userinf.usercards:
        cardlist[card['cardid']] = card
        print card['cardid'] + '\t' + card['cardname']
    sel = cardmenu()
    if(sel == 1):
        return
    {0:carddetail}[sel](cardlist)

