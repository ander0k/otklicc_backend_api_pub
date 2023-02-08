from typing import List

from uuid import UUID
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.vcn_response import Vcn_Response
from schemas.vcn_response import VcnResponseCreate, VcnResponseUpdate


class CRUDVcnResponse(CRUDBase[Vcn_Response, VcnResponseCreate, VcnResponseUpdate]):
    def create_with_demand(
        self, db: Session, *, obj_in: VcnResponseCreate, demand_id: UUID
    ) -> Vcn_Response:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, demand_id=demand_id)
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        finally:
            db.close()
        return db_obj

    def get_list_by_demand(
        self, db: Session, *, demand_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Vcn_Response]:
        try:
            rc = (
                db.query(self.model)
                .filter(Vcn_Response.demand_id == demand_id)
                .offset(skip)
                .limit(limit)
                .all()
            )
        finally:
            db.close()
        return rc

    def get_can_update(self,
                       db: Session,
                       application_user_id: UUID) -> bool:
        raise NotImplementedError
        return False

vcn_response = CRUDVcnResponse(Vcn_Response)
