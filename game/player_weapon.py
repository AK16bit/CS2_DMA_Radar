from typing import Optional

from process.address import Address
from process.cs2 import CS2


class PlayerWeapon:
    def __init__(self, address: Address):
        self.address = address

    @property
    def name(self) -> Optional[str]:
        return (
            self.address.copy()
            .offset(0x10).pointer()
            .offset(0x20).pointer()
            .str(40)
        )

    @property
    def ammo(self) -> Optional[int]:
        return (
            self.address.copy()
            .offset(CS2.offset.schemas.client_dll.C_BasePlayerWeapon.m_iClip1)
            .i16()
        )

    @property
    def max_ammo(self) -> Optional[int]:
        return (
            self.address.copy()
            .offset(0x360)
            .pointer()
            .offset(CS2.offset.schemas.client_dll.CBasePlayerWeaponVData.m_iMaxClip1)
            .i16()
        )

    @property
    def reloading(self) -> Optional[bool]:
        return (
            self.address.copy()
            .offset(CS2.offset.schemas.client_dll.C_CSWeaponBase.m_bInReload)
            .bool()
        )