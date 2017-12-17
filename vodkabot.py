# -*- coding: utf-8 -*-
from LineAlpha import LineClient
from LineAlpha.LineApi import LineTracer
from LineAlpha.LineThrift.ttypes import Message
from LineAlpha.LineThrift.TalkService import Client
import time, datetime, random ,sys, re, string, os, json

reload(sys)
sys.setdefaultencoding('utf-8')

client = LineClient()
client._qrLogin("line://au/q/")

profile, setting, tracer = client.getProfile(), client.getSettings(), LineTracer(client)
offbot, messageReq, wordsArray, waitingAnswer = [], {}, {}, {}

print client._loginresult()

helpMessage ="""═════════════════
║ Command List
╠════════════════
║❂͜͡➣ mid 
║❂͜͡➣ me 
║❂͜͡➣ open/close qr 
║❂͜͡➣ get @
║❂͜͡➣ speed 
║❂͜͡➣ woyy 
║❂͜͡➣ time
║❂͜͡➣ cek - cctv
║❂͜͡➣ bye @
║❂͜͡➣ gn 
║❂͜͡➣ steal gc
║❂͜͡➣  
║❂͜͡➣  
║❂͜͡➣ 
╠════════════════
║Creator http://line.me/ti/p/y_u_dha
═════════════════"""

wait = {
    'readPoint':{},
    'readMember':{},
    'setTime':{},
    'ROM':{}
   }

setTime = {}
setTime = wait["setTime"]

def sendMessage(to, text, contentMetadata={}, contentType=0):
    mes = Message()
    mes.to, mes.from_ = to, profile.mid
    mes.text = text

    mes.contentType, mes.contentMetadata = contentType, contentMetadata
    if to not in messageReq:
        messageReq[to] = -1
    messageReq[to] += 1
    client._client.sendMessage(messageReq[to], mes)

def NOTIFIED_ADD_CONTACT(op):
    try:
        sendMessage(op.param1, client.getContact(op.param1).displayName + "Thanks for add")
    except Exception as e:
        print (e)
        print ("\n\nNOTIFIED_ADD_CONTACT\n\n")
        return

tracer.addOpInterrupt(5,NOTIFIED_ADD_CONTACT)

def NOTIFIED_READ_MESSAGE(op):
    #print op
    try:
        if op.param1 in wait['readPoint']:
            Name = client.getContact(op.param2).displayName
            if Name in wait['readMember'][op.param1]:
                pass
            else:
                wait['readMember'][op.param1] += "\n・" + Name
                wait['ROM'][op.param1][op.param2] = "・" + Name
        else:
            pass
    except:
        pass

tracer.addOpInterrupt(55, NOTIFIED_READ_MESSAGE)

def RECEIVE_MESSAGE(op):
    msg = op.message
    try:
        if msg.contentType == 0:
            try:
                if msg.to in wait['readPoint']:
                    if msg.from_ in wait["ROM"][msg.to]:
                        del wait["ROM"][msg.to][msg.from_]
                else:
                    pass
            except:
                pass
        else:
            pass
    except KeyboardInterrupt:
	       sys.exit(0)
    except Exception as error:
        print (error)
        print ("\n\nRECEIVE_MESSAGE\n\n")
        return

tracer.addOpInterrupt(26, RECEIVE_MESSAGE)

def SEND_MESSAGE(op):
    msg = op.message
    try:
        if msg.toType == 0:
            if msg.contentType == 0:
                if msg.text == "mid":
                    sendMessage(msg.to, msg.to)
                    print "mid"
                if msg.text == "me":
                    sendMessage(msg.to, text=None, contentMetadata={'mid': msg.from_}, contentType=13)
                    print "me"
                if msg.text == "gift":
                    sendMessage(msg.to, text="gift sent", contentMetadata=None, contentType=9)
                    print "girft"
                else:
                    pass
            else:
                pass
        if msg.toType == 2:
            if msg.contentType == 0:
                if msg.text == "mid":
                    sendMessage(msg.to, msg.from_)
                    print "mid"
                if msg.text == "gid":
                    sendMessage(msg.to, msg.to)
                    print "gid"
                if msg.text == "ginfo":
                    group = client.getGroup(msg.to)
                    md = "[Group Name]\n" + group.name + "\n\n[gid]\n" + group.id + "\n\n[Group Picture]\nhttp://dl.profile.line-cdn.net/" + group.pictureStatus
                    if group.preventJoinByTicket is False: md += "\n\nInvitationURL: Permitted\n"
                    else: md += "\n\nInvitationURL: Refusing\n"
                    if group.invitee is None: md += "\nMembers: " + str(len(group.members)) + "人\n\nInviting: 0People"
                    else: md += "\nMembers: " + str(len(group.members)) + "People\nInvited: " + str(len(group.invitee)) + "People"
                    sendMessage(msg.to,md)
                    print "ginfo"
                if ("gn " in msg.text):
                    X = client.getGroup(msg.to)
                    X.name = msg.text.replace("gn ","")
                    client.updateGroup(X)
                    print "gn"
                if msg.text == "get url":
                    sendMessage(msg.to,"line://ti/g/" + client._client.reissueGroupTicket(msg.to))
                    print "get url"
                if msg.text == "open qr":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == False:
                        sendMessage(msg.to, "already open")
                    else:
                        group.preventJoinByTicket = False
                        client.updateGroup(group)
                        sendMessage(msg.to, "URL Open")
                        print "open qr"
                if msg.text in ["woii","woyyy"]:
                    group = client.getGroup(msg.to)
                    nama = [contact.mid for contact in group.members]
                    cb = ""
                    cb2 = ""
                    strt = int(0)
                    akh = int(0)
                    for md in nama:
                        akh = akh + int(6)
                        cb += """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(md)+"},"""
                        strt = strt + int(7)
                        akh = akh + 1
                        cb2 += "@nrik \n"
                    cb = (cb[:int(len(cb)-1)])
                    msg.contentType = 0
                    msg.text = cb2
                    msg.contentMetadata ={'MENTION':'{"MENTIONEES":['+cb+']}','EMTVER':'4'}
                    try:
                        client.sendMessage(msg)
                    except:
                        pass
                if "stealgc" in msg.text:
		            group = client.getGroup(msg.to)
		            sendMessage(msg.to,"Gambar Grup :\n=> http://dl.profile.line-cdn.net/" + group.pictureStatus)
                if "bye @" in msg.text:
                    _name = msg.text.replace("bye @","")
                    _nametarget = _name.rstrip('  ')
                    gs = client.getGroup(msg.to)
                    targets = []
                    for g in gs.members:
                        if _nametarget == g.displayName:
                            targets.append(g.mid)
                            for target in targets:
						        client.kickoutFromGroup(msg.to,[target])
                if "get @" in msg.text:
                    print "[Get]"
                    _name = msg.text.replace("get @","")
                    _nametarget = _name.rstrip('  ')
                    gs = client.getGroup(msg.to)
                    targets = []
                    for g in gs.members:
                        if _nametarget == g.displayName:
                            targets.append(g.mid)
                            client.findAndAddContactsByMid(g.mid)
                            for target in targets:
                                M = Message()
                                M.to = msg.to
                                M.contentType = 13
                                M.contentMetadata = {'mid': g.mid}
                                client.sendMessage(M)
                if msg.text == "close qr":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == True:
                        sendMessage(msg.to, "already close")
                    else:
                        group.preventJoinByTicket = True
                        client.updateGroup(group)
                        sendMessage(msg.to, "URL close")
                        print "close qr"
                if msg.text == "cancel all":
                    group = client.getGroup(msg.to)
                    if group.invitee is None:
                        sendMessage(op.message.to, "No one is inviting.")
                    else:
                        gInviMids = [contact.mid for contact in group.invitee]
                        client.cancelGroupInvitation(msg.to, gInviMids)
                        sendMessage(msg.to, str(len(group.invitee)) + " Done")
                        print "done cancell"
                if msg.text == "me":
                    M = Message()
                    M.to = msg.to
                    M.contentType = 13
                    M.contentMetadata = {'mid': msg.from_}
                    client.sendMessage(M)
                if msg.text == "time":
                    sendMessage(msg.to, "Current time is" + datetime.datetime.today().strftime('%Y年%m月%d日 %H:%M:%S') + "is")
                if msg.text == "gift":
                    sendMessage(msg.to, text="gift sent", contentMetadata=None, contentType=9)
                if msg.text == "cek":
                    sendMessage(msg.to, "on")
                    try:
                        del wait['readPoint'][msg.to]
                        del wait['readMember'][msg.to]
                    except:
                        pass
                    wait['readPoint'][msg.to] = msg.id
                    wait['readMember'][msg.to] = ""
                    wait['setTime'][msg.to] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                    wait['ROM'][msg.to] = {}
                    print "cek"
                if msg.text in ["Speedbot","speed"]:
				    start = time.time()
				    sendMessage(msg.to, "please wait...")
				    elapsed_time = time.time() - start
				    sendMessage(msg.to, "%ss" % (elapsed_time))
                if msg.text == "cctv":
                    if msg.to in wait['readPoint']:
                        if wait["ROM"][msg.to].items() == []:
                            chiya = ""
                        else:
                            chiya = ""
                            for rom in wait["ROM"][msg.to].items():
                                print "cctv"
                        sendMessage(msg.to, "%s\n\n\n--\n%s\n\n\n[%s]"  % (wait['readMember'][msg.to],chiya,setTime[msg.to]))
                    else:
                        sendMessage(msg.to, "blm di cek")
                if msg.text in ["Help","key"]:
                    sendMessage(msg.to, helpMessage)
                    print "key"
        else:
            pass

    except:
        pass

tracer.addOpInterrupt(25,SEND_MESSAGE)

while True:
    tracer.execute()
