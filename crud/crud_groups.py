from typing import Any,Dict,Optional,List
from fastapi import HTTPException
from sqlalchemy.sql.expression import delete
from starlette import status

from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.groups import Group
from schemas.groups import TreeName,GroupDel,GroupPost,GroupPut


group_views = {
    "profession" : 'v_grp_prof',
    "geos"       : 'v_grp_geo',
    "metatags"   : 'v_grp_tags',
    "companies"  : 'v_grp_comps',
}

group_movs = {
    "profession" : 'mov_grp_prof',
    "geos"       : 'mov_grp_geo',
    "metatags"   : 'mov_grp_tags',
}

group_dels = {
    "profession" : 'del_grp_prof',
    "geos"       : 'del_grp_geo',
    "metatags"   : 'del_grp_tags',
}

class CRUDGroup(CRUDBase[Group,Group,Group]):
    def get_list(self, db: Session, *, group: TreeName) -> dict:
        groups = {}
        query = "select parent_val,child_val,syn from {} t".format(group_views[group])
        try:
            result = db.execute(query)
            for row in result:
                pv = row['parent_val']
                grp = groups.get(pv, None)
                if not grp:
                    grp = []
                    groups[pv] = grp
                grp.append({"child_val": row['child_val'], "syn": row['syn']})
        finally:
            db.close()
        return groups

    def post(self, db: Session, *, group: GroupPost) -> dict:
        query = "insert into {}(parent_val,child_val,syn) values(:parent_val,:child_val,:syn)".format(group_views[group.group])
        try:
            db.execute(query, {"parent_val": group.parent_val, "child_val": group.child_val, "syn": group.syn})
            db.commit()
        finally:
            db.close()
        return {}

    def put(self, db: Session, *, group: GroupPut) -> dict:
        query = 'call {}(:child,:parent,:new_name)'.format(group_movs[group.group])
        try:
            db.execute(query, {
                "child" : group.child,
                "parent": group.parent,
                "new_name" : group.new_name,
            })
            db.commit()
        finally:
            db.close()
        return {}

    def delete(self, db: Session, *, group: GroupDel) -> dict:
        query = 'call {}(:parent,:child)'.format(group_dels[group.group])
        try:
            db.execute(query, {
                "parent": group.parent,
                "child" : group.child,
            })
            db.commit()
        finally:
            db.close()
        return {}

    def create(self, db: Session, *, group: Group) -> Group:
        try:
            db.add(group)
            db.commit()
            db.refresh(group)
        finally:
            db.close()
        return group



group = CRUDGroup(Group)
