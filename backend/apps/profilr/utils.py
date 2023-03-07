from apps.services import incident_api_service
from django.conf import settings


def get_filter_options(filters, user_token):
    FILTERS = "filters"
    BUURTEN = "buurten"
    AFDELINGEN = "afdelingen"
    ONDERWERPEN = "onderwerpen"
    ONDERWERP_ITEMS = "onderwerpItems"

    departments = incident_api_service.get_afdelingen(user_token)
    categories = incident_api_service.get_onderwerpgroepen(user_token)
    areas = incident_api_service.get_wijken(user_token)

    afdeling_relaties = [
        incident_api_service.get_afdeling_relaties(user_token, a)
        for a in filters.get(AFDELINGEN, {})
    ]
    afdeling_relaties = {
        BUURTEN: [
            *set([str(o) for a in afdeling_relaties for o in a.get(BUURTEN, [])])
        ],
        ONDERWERPEN: [
            *set([str(o) for a in afdeling_relaties for o in a.get(ONDERWERPEN, [])])
        ],
    }
    # create lookups for filter options
    afdelingen_dict = {d.get("code"): d.get("omschrijving") for d in departments}
    buurten_dict = {
        b.get("code"): b.get("omschrijving") for w in areas for b in w.get(BUURTEN, [])
    }
    onderwerpen_dict = {
        b.get("code"): b.get("omschrijving")
        for w in categories
        for b in w.get(ONDERWERPEN, [])
    }
    # add readable filter results like: [[id, name]]
    filter_types = (
        (BUURTEN, buurten_dict),
        (AFDELINGEN, afdelingen_dict),
        (ONDERWERP_ITEMS, onderwerpen_dict),
    )
    filters = {
        ft[0]: [[o, ft[1].get(o, o)] for o in filters.get(ft[0], [])]
        for ft in filter_types
    }

    # add filters count for nested filter sets
    areas = [
        {
            **d,
            BUURTEN: [
                o
                for o in d.get(BUURTEN)
                if not settings.ENABLE_AFDELING_RELATIES_ENDPOINT
                or o.get("code") in afdeling_relaties.get(BUURTEN, [])
            ],
            FILTERS: [
                b
                for b in filters[BUURTEN]
                if b[0]
                in [
                    bb.get("code")
                    for bb in d.get(BUURTEN, [])
                    if not settings.ENABLE_AFDELING_RELATIES_ENDPOINT
                    or bb.get("code") in afdeling_relaties.get(BUURTEN, [])
                ]
            ],
        }
        for d in areas
        if [
            o
            for o in d.get(BUURTEN)
            if not settings.ENABLE_AFDELING_RELATIES_ENDPOINT
            or o.get("code") in afdeling_relaties.get(BUURTEN, [])
        ]
    ]

    categories = [
        {
            **d,
            ONDERWERPEN: [
                o
                for o in d.get(ONDERWERPEN)
                if not settings.ENABLE_AFDELING_RELATIES_ENDPOINT
                or o.get("code") in afdeling_relaties.get(ONDERWERPEN, [])
            ],
            FILTERS: [
                b
                for b in filters[ONDERWERP_ITEMS]
                if b[0]
                in [
                    bb.get("code")
                    for bb in d.get(ONDERWERPEN, [])
                    if not settings.ENABLE_AFDELING_RELATIES_ENDPOINT
                    or bb.get("code") in afdeling_relaties.get(ONDERWERPEN, [])
                ]
            ],
        }
        for d in categories
        if [
            o
            for o in d.get(ONDERWERPEN)
            if not settings.ENABLE_AFDELING_RELATIES_ENDPOINT
            or o.get("code") in afdeling_relaties.get(ONDERWERPEN, [])
        ]
    ]

    return filters, departments, categories, areas
