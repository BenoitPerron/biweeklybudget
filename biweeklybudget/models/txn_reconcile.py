"""
The latest version of this package is available at:
<http://github.com/jantman/biweeklybudget>

################################################################################
Copyright 2016 Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>

    This file is part of biweeklybudget, also known as biweeklybudget.

    biweeklybudget is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    biweeklybudget is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with biweeklybudget.  If not, see <http://www.gnu.org/licenses/>.

The Copyright and Authors attributions contained herein may not be removed or
otherwise altered, except to add the Author attribution of a contributor to
this work. (Additional Terms pursuant to Section 7b of the AGPL v3)
################################################################################
While not legally required, I sincerely request that anyone who finds
bugs please submit them at <https://github.com/jantman/biweeklybudget> or
to me via email, and that you send any contributions or improvements
either as a pull request on GitHub, or to me via email.
################################################################################

AUTHORS:
Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>
################################################################################
"""

from biweeklybudget.utils import dtnow
from sqlalchemy import (
    Column, Integer, String, ForeignKey, ForeignKeyConstraint, UniqueConstraint,
    Index
)
from sqlalchemy_utc import UtcDateTime
from sqlalchemy.orm import relationship, backref
from biweeklybudget.models.base import Base, ModelAsDict


class TxnReconcile(Base, ModelAsDict):

    __tablename__ = 'txn_reconciles'
    # NOTE: __table_args__ is after column definitions

    #: Primary Key
    id = Column(Integer, primary_key=True)

    #: Transaction ID
    txn_id = Column(Integer, ForeignKey('transactions.id'), nullable=False)

    #: Relationship - :py:class:`~.Transaction`
    transaction = relationship(
        "Transaction", backref=backref("reconcile", uselist=False),
        foreign_keys=[txn_id]
    )

    #: OFX Transaction FITID
    ofx_fitid = Column(String(255))

    #: OFX Transaction Account ID
    ofx_account_id = Column(Integer)

    #: Relationship - :py:class:`~.OFXTransaction`
    ofx_trans = relationship(
        "OFXTransaction", backref=backref("reconcile", uselist=False),
        foreign_keys=[ofx_fitid, ofx_account_id]
    )

    #: ReconcileRule ID; set if this reconcile was created by a rule
    rule_id = Column(Integer, ForeignKey('reconcile_rules.id'))

    #: Relationship - :py:class:`~.ReconcileRule` that created this reconcile,
    #: if any.
    rule = relationship("ReconcileRule")

    #: Notes
    note = Column(String(254))

    #: time when this reconcile was made
    reconciled_at = Column(UtcDateTime, default=dtnow())

    __table_args__ = (
        ForeignKeyConstraint(
            ['ofx_account_id', 'ofx_fitid'],
            ['ofx_trans.account_id', 'ofx_trans.fitid']
        ),
        UniqueConstraint('txn_id'),
        UniqueConstraint('ofx_account_id', 'ofx_fitid'),
        Index(
            'fk_txn_reconciles_txn_id_transactions',
            txn_id
        ),
        Index(
            'fk_txn_reconciles_ofx_account_id_ofx_trans',
            ofx_account_id,
            ofx_fitid
        ),
        {'mysql_engine': 'InnoDB'}
    )

    def __repr__(self):
        return "<TxnReconcile(id=%d)>" % (
            self.id
        )
