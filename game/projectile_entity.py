from typing import Optional, Tuple

from process.address import Address
from process.cs2 import CS2
from utils import Vec3


class ProjectileEntity:
    def __init__(self, address: Address) -> None:
        self.address = address

    @property
    def pos(self) -> Optional[Vec3]:
        return (
            self.address.copy()
            .offset(CS2.offset.schemas.client_dll.C_BaseCSGrenadeProjectile.vecLastTrailLinePos)
            .vec3()
        )

    @property
    def pos_throw(self) -> Optional[Vec3]:
        return (
            self.address.copy()
            .offset(CS2.offset.schemas.client_dll.C_BaseCSGrenadeProjectile.m_vInitialPosition)
            .vec3()
        )

    @property
    def spawn_time(self) -> float:
        return (
            self.address.copy()
            .offset(CS2.offset.schemas.client_dll.C_BaseCSGrenadeProjectile.m_flSpawnTime)
            .float()
        )

    @property
    def detonate_time(self) -> Optional[float]:
        return (
            self.address.copy()
            .offset(CS2.offset.schemas.client_dll.C_BaseGrenade.m_flDetonateTime)
            .float()
        )

    # @property
    # def owner(self) -> :
    # C_BaseGrenade m_hOriginalThrower



class SmokeProjectileEntity(ProjectileEntity):
    def __init__(self, address: Address) -> None:
        super().__init__(address)


    @property
    def pos_detonation(self) -> Vec3:
        return (
            self.address.copy()
            .offset(CS2.offset.schemas.client_dll.C_SmokeGrenadeProjectile.m_vSmokeDetonationPos)
            .vec3()
        )

    @property
    def color(self) -> Vec3:
        return (
            self.address.copy()
            .offset(CS2.offset.schemas.client_dll.C_SmokeGrenadeProjectile.m_vSmokeColor)
            .vec3()
        )


class HegrenadeProjectileEntity(ProjectileEntity):
    def __init__(self, address: Address) -> None:
        super().__init__(address)


class MolotovProjectileEntity(ProjectileEntity):
    def __init__(self, address: Address) -> None:
        super().__init__(address)


class FlashbangProjectileEntity(ProjectileEntity):
    def __init__(self, address: Address) -> None:
        super().__init__(address)


class DecayProjectileEntity(ProjectileEntity):
    def __init__(self, address: Address) -> None:
        super().__init__(address)

