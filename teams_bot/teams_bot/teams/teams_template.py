# def teams_response(msg):
#     button = []
#     if msg.get('buttons'):
#         for btns in msg['buttons']:
#             btn_title = btns['title']
#             if btns.get('text'):
#                 if btns['text'] != "":
#                     btn_title = btns['text']
#             # btns['text'] if btns.get('text') or btns.get('text') is not "" else btns['title']
#             btn = {
#                 "type": "messageBack",
#                 "title": btn_title,
#                 "displayText": btn_title,
#                 "text": btns['payload'],
#             }
#             button.append(btn)
#         card = {
#             'type': 'message',
#             'attachments': [
#                 {
#                     "contentType": "application/vnd.microsoft.card.hero",
#                     "content": {
#                         "text": msg['text'],
#                         "buttons": button
#                     }
#                 }
#             ]
#         }
#     elif msg.get('text'):
#         card = {
#             'textFormat': 'xml',
#             'type': 'message',
#             'text': msg['text']
#         }
#     elif msg.get('data'):
#         card = {
#             'type': 'message',
#             'text': msg['data']
#         }
#     if msg.get('template_type') == 'html':
#         card['textFormat'] = 'xml'
#     return card
def teams_response(msg, params):
    button = []
    card_list = []
    if msg.get('add_calendar'):
        calendar_card = calender_card_template
        return calendar_card
    if msg.get('append_text'):
        param_list = []
        for i in msg['append_text']:
            param_list.append(params[i])
        text_msg = msg['text'].format(*param_list)
    else:
        text_msg = msg.get('text', 'sorry, error has occured')
    if msg.get('buttons'):
        for btns in msg['buttons']:
            if msg.get('append_buttons'):
                param_list = []
                for i in msg['append_buttons']:
                    param_list.append(params[i])
                btn_title = btns['title'].format(*param_list)
                btn_payload = btns['payload'].format(*param_list)
                if btns.get('text'):
                    if btns['text'] != "":
                        btn_title = btns['text'].format(*param_list)
            else:
                btn_payload = btns['payload']
                btn_title = btns['title']
                if btns.get('text'):
                    if btns['text'] != "":
                        btn_title = btns['text']
            # btns['text'] if btns.get('text') or btns.get('text') is not "" else btns['title']
            btn = {
                "type": "messageBack",
                "title": btn_title,
                "displayText": btn_title,
                "text": btn_payload,
            }
            button.append(btn)
        button_list = [button[i:i + 50] for i in range(0, len(button), 50)]

        card = {
            'type': 'message',
            'attachments': [
                {
                    "contentType": "application/vnd.microsoft.card.hero",
                    "content": {
                        "text": text_msg,
                        "buttons": button_list[0]
                    }
                }
            ]
        }
        card_list.append(card)
        for n in range(1, len(button_list) - 1):
            card = {
                'type': 'message',
                'attachments': [
                    {
                        "contentType": "application/vnd.microsoft.card.hero",
                        "content": {
                            "buttons": button_list[n]
                        }
                    }
                ]
            }
            card_list.append(card)

    elif msg.get('text'):
        card = {
            'textFormat': 'xml',
            'type': 'message',
            'text': text_msg
        }
        card_list.append(card)

    elif msg.get('data'):
        card = {
            'type': 'message',
            'text': msg['data']
        }
    if msg.get('template_type') == 'html':
        card['textFormat'] = 'xml'
        card_list.append(card)
    if msg.get('form'):
        print("form received", msg)
        if msg['form']['content']['name'] == 'ticketUpdate_form':
            card_list = updateTicketTemplate(msg['form']['content']['fields'])
        elif msg['form']['content']['name'] == 'star_form':
            card_list = star_card
        elif msg['form']['content']['name'] == 'feedback_form':
            card_list = feedback_card
    print(card_list)
    return card_list


calender_card_template = [{
    'type': 'message',
    'attachments': [
        {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.0",
                "body": [
                    {
                        "type": "Container",
                        "items": [
                            {
                                "type": "TextBlock",
                                "text": "Please select a date"
                            }
                        ]
                    }
                ],
                "actions": [

                    {
                        "type": "Action.ShowCard",
                        "title": "Select the date",
                        "card": {
                            "type": "AdaptiveCard",
                            "version": "1.0",
                            "body": [
                                {
                                    "type": "Input.Date",
                                    "id": "selected_date",
                                }
                            ],
                            "actions": [
                                {
                                    "type": "Action.Submit",
                                    "title": "Submit"
                                }
                            ]
                        }
                    },
                    {
                        "type": "Action.Submit",
                        "title": "Cancel"
                    }
                ]
            }
        }
    ]
}]

feedback_card = [{
    'type': 'message',
    'attachments': [
        {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.0",
                "body": [
                    {
                        "type": "Container",
                        "items": [
                            {
                                "type": "TextBlock",
                                "text": "Thankyou! Would you like to share your feedback ?"
                            }
                        ]
                    }
                ],
                "actions": [

                    {
                        "type": "Action.ShowCard",
                        "title": "Yes",
                        "card": {
                            "type": "AdaptiveCard",
                            "version": "1.0",
                            "body": [
                                {
                                    "type": "Input.Text",
                                    "id": "feedback",
                                    "isMultiline": "true",
                                    "placeholder": "Enter your feedback",
                                    "isRequired": "true",
                                    "errorMessage": "Please enter your feedback"
                                }
                            ],
                            "actions": [
                                {
                                    "type": "Action.Submit",
                                    "title": "Submit"
                                }
                            ]
                        }
                    },
                    {
                        "type": "Action.Submit",
                        "title": "No"
                    }
                ]
            }
        }
    ]
}]

star_card = [{
    'type': 'message',
    'attachments': [
        {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.0",
                "body": [
                    {
                        "type": "TextBlock",
                        "text": "Please rate your experience with bot."
                    },
                    {
                        "type": "Input.ChoiceSet",
                        "id": "bot_rating",
                        "style": "expanded",
                        "isMultiSelect": "false",
                        "isRequired": "true",
                        "errorMessage": "Please select one.",
                        "choices": [
                            {
                                "title": 1,
                                "value": 1
                            },
                            {
                                "title": 2,
                                "value": 2
                            },
                            {
                                "title": 3,
                                "value": 3
                            },
                            {
                                "title": 4,
                                "value": 4
                            },
                            {
                                "title": 5,
                                "value": 5
                            },

                        ]
                    }
                ],

                "actions": [
                    {
                        "type": "Action.Submit",
                        "title": "OK"
                    }
                ],
            }
        }
    ]

}]


def updateTicketTemplate(fields):
    facts = []
    for field in fields:
        if field["required"] == "disabled":
            fact = {
                "title": field['name'],
                "value": field['value']
            }
            facts.append(fact)

    update_ticket = [{
        'type': 'message',
        'attachments': [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.0",
                    "body": [
                        {
                            "type": "Container",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": "Please Find your tickets description below",
                                    "wrap": "true"
                                },
                                {
                                    "type": "FactSet",
                                    "facts": facts
                                }
                            ]
                        }
                    ],
                    "actions": [
                        {
                            "type": "Action.ShowCard",
                            "title": "Update Ticket Description",
                            "card": {
                                "type": "AdaptiveCard",
                                "version": "1.0",
                                "body": [
                                    {
                                        "type": "Input.Text",
                                        "id": "ticketDescription",
                                        "isMultiline": "true",
                                        "placeholder": "Enter your Description",
                                        "isRequired": "true",
                                        "errorMessage": "please enter the description"
                                    },
                                    {
                                        "type": "Input.ChoiceSet",
                                        "id": "incident_no",
                                        "isVisible": "false",
                                        "style": "compact",
                                        "isMultiSelect": "false",
                                        "value": fields[0]['value'],
                                        "choices": [
                                            {
                                                "title": fields[0]['name'],
                                                "value": fields[0]['value']
                                            }

                                        ]
                                    },
                                    {
                                        "type": "Input.ChoiceSet",
                                        "id": "summary",
                                        "isVisible": "false",
                                        "style": "compact",
                                        "isMultiSelect": "false",
                                        "value": fields[2]['value'],
                                        "choices": [
                                            {
                                                "title": fields[2]['name'],
                                                "value": fields[2]['value']
                                            }

                                        ]
                                    }
                                ],

                                "actions": [
                                    {
                                        "type": "Action.Submit",
                                        "title": "OK"
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        ]

    }]
    return update_ticket


# adaptive_card = [{
#     "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
#     "type": "AdaptiveCard",
#     "version": "1.0",
#     "body": [
#         {
#             "type": "Container",
#             "items": [
#                 {
#                     "type": "TextBlock",
#                     "text": "Thankyou! Would you like to share your feedback ?"
#                 }
#             ]
#         }
#     ],
#     "actions": [
#         {
#             "type": "Action.Submit",
#             "title": "NO"
#         },
#         {
#             "type": "Action.ShowCard",
#             "title": "Yes",
#             "card": {
#                 "type": "AdaptiveCard",
#                 "version": "1.0",
#                 "body": [
#                     {
#                         "type": "Input.Text",
#                         "id": "comment",
#                         "isMultiline": "true",
#                         "placeholder": "Enter your comment"
#                     }
#                 ],
#                 "actions": [
#                     {
#                         "type": "Action.Submit",
#                         "title": "Submit"
#                     }
#                 ]
#             }
#         }
#     ]
# }]

temp = {
    'textFormat': 'xml',
    'type': 'message',
    "text": '\\n               <style>\\n               table.tickets_status, .tickets_status td, .tickets_status th { \\n               border: 1px solid #ddd;\\n               text-align: left;\\n               }\\n               \\n               table.tickets_status {\\n               border-collapse: collapse;\\n               width: 235px;\\n               margin: 2px;\\n               }\\n               \\n               .tickets_status th, .tickets_status td{\\n               padding: 8px;\\n               }\\n               </style>\\n               <p>Please Find list of active users.</p>\\n               <table class=\\"tickets_status\\">\\n               <tr>\\n               <th>Username</th>\\n               <th>User Type</th>\\n               <th>Last Login</th>\\n               \\n               </tr>\\n               undefined<tr><td>VI_NOC2</td><td>User</td><td>Never logged in</td></tr><tr><td>GCC_NOC</td><td>User</td><td>Never logged in</td></tr><tr><td>Elogisol</td><td>User</td><td>Never logged in</td></tr><tr><td>Techmbs</td><td>User</td><td>Never logged in</td></tr><tr><td>IQI Solutions</td><td>User</td><td>Never logged in</td></tr><tr><td>Sagar bhosale</td><td>User</td><td>Never logged in</td></tr><tr><td>Swapnil Hule</td><td>User</td><td>Never logged in</td></tr><tr><td>Ashish Choudhari</td><td>User</td><td>Never logged in</td></tr><tr><td>gstn_user</td><td>User</td><td>Never logged in</td></tr><tr><td>SanjayGera</td><td>User</td><td>Never logged in</td></tr><tr><td>Nakul</td><td>User</td><td>Never logged in</td></tr><tr><td>NOC2</td><td>User</td><td>Never logged in</td></tr><tr><td>BSID Admin</td><td>User</td><td>Never logged in</td></tr><tr><td>bristlecone_01</td><td>User</td><td>Never logged in</td></tr><tr><td>SingaporeTeam</td><td>User</td><td>Never logged in</td></tr><tr><td>Sharat</td><td>User</td><td>Never logged in</td></tr><tr><td>dams</td><td>User</td><td>Never logged in</td></tr><tr><td>Capgemini</td><td>User</td><td>Never logged in</td></tr><tr><td>Advik</td><td>User</td><td>Never logged in</td></tr><tr><td>HDFC</td><td>User</td><td>Never logged in</td></tr><tr><td>Jay Switch</td><td>User</td><td>Never logged in</td></tr><tr><td>Paresh</td><td>User</td><td>Never logged in</td></tr><tr><td>Yazaki</td><td>User</td><td>Never logged in</td></tr><tr><td>MNS</td><td>User</td><td>Never logged in</td></tr><tr><td>GMushroom</td><td>User</td><td>Never logged in</td></tr><tr><td>Vishal</td><td> Super Admin</td><td>Never logged in</td></tr><tr><td>Endurance</td><td>User</td><td>Never logged in</td></tr><tr><td>Cooper</td><td>User</td><td>Never logged in</td></tr><tr><td>Vedika</td><td>User</td><td>Never logged in</td></tr><tr><td>Novac</td><td>User</td><td>Never logged in</td></tr><tr><td>vartika</td><td> Super Admin</td><td>Never logged in</td></tr><tr><td>Admin</td><td> Super Admin</td><td>11/19/2020, 1:23:33 PM</td></tr><tr><td>shweta</td><td> Super Admin</td><td>12/2/2020, 11:11:46 AM</td></tr><tr><td>Neha</td><td> Super Admin</td><td>Never logged in</td></tr><tr><td>Ayush</td><td> Super Admin</td><td>Never logged in</td></tr><tr><td>GPIL</td><td>User</td><td>Never logged in</td></tr><tr><td>EmpAxis</td><td>User</td><td>Never logged in</td></tr><tr><td>japan_f</td><td>User</td><td>Never logged in</td></tr><tr><td>kei_industries</td><td>User</td><td>Never logged in</td></tr><tr><td>Kose</td><td>User</td><td>Never logged in</td></tr><tr><td>AmitM_MetalOne</td><td>User</td><td>Never logged in</td></tr><tr><td>GirishC_MetalOne</td><td>User</td><td>Never logged in</td></tr><tr><td>Hiroshi.nakanishi</td><td>User</td><td>Never logged in</td></tr><tr><td>midrex</td><td>User</td><td>Never logged in</td></tr><tr><td>binary_sem</td><td>User</td><td>Never logged in</td></tr><tr><td>Naresh</td><td>User</td><td>Never logged in</td></tr><tr><td>Shailendra</td><td>User</td><td>Never logged in</td></tr><tr><td>internal_it</td><td>User</td><td>Never logged in</td></tr><tr><td>viney</td><td>User</td><td>Never logged in</td></tr><tr><td>S2 Alerts</td><td>User</td><td>Never logged in</td></tr><tr><td>GMP_Monitoring</td><td>User</td><td>Never logged in</td></tr><tr><td>SSNCHENNAI</td><td>User</td><td>Never logged in</td></tr><tr><td>Gaurav</td><td>User</td><td>Never logged in</td></tr><tr><td>siva</td><td>User</td><td>Never logged in</td></tr><tr><td>AVHA_USER</td><td>User</td><td>Never logged in</td></tr><tr><td>HariOm</td><td>User</td><td>Never logged in</td></tr><tr><td>BSKheda</td><td>User</td><td>Never logged in</td></tr><tr><td>yaantra</td><td>User</td><td>Never logged in</td></tr><tr><td>gpil_admin</td><td>User</td><td>Never logged in</td></tr><tr><td>BSchakan</td><td>User</td><td>Never logged in</td></tr><tr><td>ASK_Monitoring</td><td>User</td><td>Never logged in</td></tr><tr><td>Love_Vivah_User</td><td>User</td><td>Never logged in</td></tr><tr><td>Chakan SMS Users</td><td>User</td><td>Never logged in</td></tr><tr><td>Kheda SMS Users</td><td>User</td><td>Never logged in</td></tr><tr><td>cloud_support</td><td>User</td><td>Never logged in</td></tr><tr><td>Datamatics_user</td><td>User</td><td>Never logged in</td></tr><tr><td>NOC</td><td>User</td><td>Never logged in</td></tr><tr><td>NGK_Monitoring</td><td>User</td><td>Never logged in</td></tr><tr><td>ERGUS_User</td><td>User</td><td>Never logged in</td></tr><tr><td>Firewall Azure tunnel and ISP</td><td>User</td><td>Never logged in</td></tr><tr><td>Lingual_user</td><td>User</td><td>Never logged in</td></tr><tr><td>Arjas_Monitoring</td><td>User</td><td>Never logged in</td></tr><tr><td>Tushar</td><td>User</td><td>Never logged in</td></tr><tr><td>mansur</td><td>User</td><td>Never logged in</td></tr><tr><td>Praveen</td><td> Super Admin</td><td>Never logged in</td></tr><tr><td>VI_NOC</td><td>User</td><td>Never logged in</td></tr><tr><td>IBL_NOC</td><td>User</td><td>Never logged in</td></tr><tr><td>ERP Internal</td><td>User</td><td>Never logged in</td></tr><tr><td>Sharepoint Internal</td><td>User</td><td>Never logged in</td></tr><tr><td>Sumit Sahu</td><td>User</td><td>Never logged in</td></tr><tr><td>Abhishek Jharekar</td><td>User</td><td>Never logged in</td></tr><tr><td>Jeevesh Morey</td><td>User</td><td>Never logged in</td></tr><tr><td>newservicedesk</td><td>User</td><td>Never logged in</td></tr><tr><td>Spice_VAS</td><td>User</td><td>Never logged in</td></tr><tr><td>Amada_User</td><td>User</td><td>Never logged in</td></tr><tr><td>Jindal_user</td><td>User</td><td>Never logged in</td></tr><tr><td>neeraj.jha</td><td>User</td><td>Never logged in</td></tr><tr><td>Prasenjit Roy</td><td>User</td><td>Never logged in</td></tr><tr><td>Multicraft</td><td>User</td><td>Never logged in</td></tr><tr><td>Delhi Cargo</td><td>User</td><td>Never logged in</td></tr><tr><td>Kunal</td><td>User</td><td>Never logged in</td></tr><tr><td>Vikas</td><td>User</td><td>Never logged in</td></tr><tr><td>20952</td><td>User</td><td>Never logged in</td></tr><tr><td>GODB</td><td>User</td><td>Never logged in</td></tr>\\n               </table>'
}
message = {
    'simple_card': {
        "type": "message",
        "text": "Plain text is ok, but sometimes I long for more...",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "version": "1.0",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": "Hello World!",
                            "size": "large"
                        },
                        {
                            "type": "TextBlock",
                            "text": "*Sincerely yours,*"
                        },
                        {
                            "type": "TextBlock",
                            "text": "Adaptive Cards",
                            "separation": "none"
                        }
                    ],
                    "actions": [
                        {
                            "type": "Action.OpenUrl",
                            "url": "http://adaptivecards.io",
                            "title": "Learn More"
                        }
                    ]
                }
            }
        ]
    },
    'hero_card': {
        'type': 'message',
        "text": "hi",
        'attachments': [
            {
                "contentType": "application/vnd.microsoft.card.hero",
                "content": {
                    "buttons": [
                        {
                            "type": "messageBack",
                            "title": "postback button",
                            "displayText": "I clicked this button",
                            "text": "User just clicked the MessageBack button",
                        },
                        {
                            "type": "messageBack",
                            "title": "Wikipeda page",
                            "displayText": "I clicked this button",
                            "text": "https://en.wikipedia.org/wiki/Seattle_Center_Monorail"
                        }
                    ]
                }
            }
        ]
    },
    'adaptive_card': {
        'type': 'message',
        'attachments': [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.0",
                    "body": [
                        {
                            "type": "Container",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": "Publish Adaptive Card schema",
                                    "weight": "bolder",
                                    "size": "medium"
                                },
                                {
                                    "type": "ColumnSet",
                                    "columns": [
                                        {
                                            "type": "Column",
                                            "width": "auto",
                                            "items": [
                                                {
                                                    "type": "Image",
                                                    "url": "https://pbs.twimg.com/profile_images/3647943215/d7f12830b3c17a5a9e4afcc370e3a37e_400x400.jpeg",
                                                    "size": "small",
                                                    "style": "person"
                                                }
                                            ]
                                        },
                                        {
                                            "type": "Column",
                                            "width": "stretch",
                                            "items": [
                                                {
                                                    "type": "TextBlock",
                                                    "text": "Matt Hidinger",
                                                    "weight": "bolder",
                                                    "wrap": 'true'
                                                },
                                                {
                                                    "type": "TextBlock",
                                                    "spacing": "none",
                                                    "text": "Created {{DATE(2017-02-14T06:08:39Z, SHORT)}}",
                                                    "isSubtle": 'true',
                                                    "wrap": 'true'
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "Container",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": "Now that we have defined the main rules and features of the format, we need to produce a schema and publish it to GitHub. The schema will be the starting point of our reference documentation.",
                                    "wrap": 'true'
                                },
                                {
                                    "type": "FactSet",
                                    "facts": [
                                        {
                                            "title": "Board:",
                                            "value": "Adaptive Card"
                                        },
                                        {
                                            "title": "List:",
                                            "value": "Backlog"
                                        },
                                        {
                                            "title": "Assigned to:",
                                            "value": "Matt Hidinger"
                                        },
                                        {
                                            "title": "Due date:",
                                            "value": "Not set"
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "actions": [
                        {
                            "type": "Action.ShowCard",
                            "title": "Set due date",
                            "card": {
                                "type": "AdaptiveCard",
                                "body": [
                                    {
                                        "type": "Input.Date",
                                        "id": "dueDate"
                                    }
                                ],
                                "actions": [
                                    {
                                        "type": "Action.Submit",
                                        "title": "OK"
                                    }
                                ]
                            }
                        },
                        {
                            "type": "Action.ShowCard",
                            "title": "Comment",
                            "card": {
                                "type": "AdaptiveCard",
                                "body": [
                                    {
                                        "type": "Input.Text",
                                        "id": "comment",
                                        "isMultiline": 'true',
                                        "placeholder": "Enter your comment"
                                    }
                                ],
                                "actions": [
                                    {
                                        "type": "Action.Submit",
                                        "title": "OK"
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        ]
    },
    'office_card': {
        'type': 'message',
        'attachments': [
            {
                "contentType": "application/vnd.microsoft.teams.card.o365connector",
                "content": {
                    "@type": "MessageCard",
                    "@context": "http://schema.org/extensions",
                    "summary": "John Doe commented on Trello",
                    "title": "Project Tango",
                    "sections": [
                        {
                            "activityTitle": "John Doe commented",
                            "activitySubtitle": "On Project Tango",
                            "activityText": "\"Here are the designs\"",
                            "activityImage": "http://connectorsdemo.azurewebsites.net/images/MSC12_Oscar_002.jpg"
                        },
                        {
                            "title": "Details",
                            "facts": [
                                {
                                    "name": "Labels",
                                    "value": "Designs, redlines"
                                },
                                {
                                    "name": "Due date",
                                    "value": "Dec 7, 2016"
                                },
                                {
                                    "name": "Attachments",
                                    "value": "[final.jpg](http://connectorsdemo.azurewebsites.net/images/WIN14_Jan_04.jpg)"
                                }
                            ]
                        },
                        {
                            "title": "Images",
                            "images": [
                                {
                                    "image": "http://connectorsdemo.azurewebsites.net/images/MicrosoftSurface_024_Cafe_OH-06315_VS_R1c.jpg"
                                },
                                {
                                    "image": "http://connectorsdemo.azurewebsites.net/images/WIN12_Scene_01.jpg"
                                },
                                {
                                    "image": "http://connectorsdemo.azurewebsites.net/images/WIN12_Anthony_02.jpg"
                                }
                            ]
                        }
                    ],
                    "potentialAction": [
                        {
                            "@context": "http://schema.org",
                            "@type": "ViewAction",
                            "name": "View in Trello",
                            "target": [
                                "https://trello.com/c/1101/"
                            ]
                        }
                    ]
                }
            }
        ]
    }
}
