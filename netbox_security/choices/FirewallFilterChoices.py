from utilities.choices import ChoiceSet


class FamilyChoices(ChoiceSet):

    INET = 'inet'
    INET6 = 'inet6'
    ANY = 'any'
    MPLS = 'mpls'
    CCC = 'ccc'

    CHOICES = [
        (INET, 'INET', 'green'),
        (INET6, 'INET6', 'red'),
        (ANY, 'ANY', 'blue'),
        (MPLS, 'MPLS', 'cyan'),
        (CCC, 'CCC', 'orange'),
    ]
