class Action:
    def __init__(self, name, action_type, master, actor, actor_type, targets):
        self.name = name
        self.action_type = action_type  # order action is a command from a superior entity/alternative is independent action
        self.master = master
        self.actor = actor  # entity that performs action
        self.actor_type = actor_type
        self.targets = targets


class ActionsManager(object):
    # describes all possible actions between Core Entities
    # actions are static by design and are not expected to be changed during the course of the game
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ActionsManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.allowed_actions = [Action(name='order supply run', action_type='order', master='MainForce',
                                       actor='SupportUnit', actor_type='LOGISTIC',
                                       targets=['Castle', 'Town', 'Village']),
                                Action(name='kill', action_type='order', master='MainForce',
                                       actor='SupportUnit', actor_type='LOGISTIC',
                                       targets=['Town'])
                                ]

    def get_actions_by_target(self, target):
        action_set = []
        for action in self.allowed_actions:
            if target in action.targets:
                action_set.append(action)

