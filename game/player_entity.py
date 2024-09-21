from typing import overload, Optional, Any, Dict, Self

from process.address import Address
from process.cs2 import CS2
from utils import Vec3, Vec2


class PlayerEntity:
    _cache: Dict[int, Dict[int, Dict[str, Any]]] = dict()

    @overload
    def __init__(self, entity_list_address: Address, player_index: int): ...

    @overload
    def __init__(self, player_controller: Address, player_pawn: Address): ...

    def __init__(self, *args, **kwargs):
        if len(args) != 2: raise ValueError

        self._player_controller: Optional[Address] = None
        self._player_pawn: Optional[Address] = None

        self._init_type: Optional[int] = None
        if isinstance(args[0], Address) and isinstance(args[1], int):
            self._init_type = 0
            self._entity_list_address, self._player_index = args

        elif isinstance(args[0], Address) and isinstance(args[1], Address):
            self._init_type = 1

            self._player_controller_address, self._player_pawn_address = args
        else: raise ValueError

    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, PlayerEntity): return False

        return all((
            self.controller.address == other.controller.address,
            self.pawn.address == other.pawn.address
        ))

    @staticmethod
    def _get_list_entry_address(entity_list_address: Address, offset: int) -> Address:
        return entity_list_address.copy().offset(0x10 + 0x08 * ((offset & 0x7FFF) >> 9)).pointer()

    @staticmethod
    def _get_list_entry_offset(offset: int) -> int:
        return 0x78 * (offset & 0x1FF)

    @property
    def controller(self) -> Optional[Address]:
        if self._player_controller is None:
            match self._init_type:
                case 0:
                    # list entry
                    controller_list_entry_address = self._get_list_entry_address(
                        self._entity_list_address, self._player_index
                    )
                    if not controller_list_entry_address.address: return None

                    # controller address
                    player_controller_address = controller_list_entry_address.offset(
                        self._get_list_entry_offset(self._player_index)
                    ).pointer()
                    if not player_controller_address.address: return None

                    self._player_controller = player_controller_address
                case 1: self._player_controller = self._player_controller_address
                case _: return None

        return self._player_controller

    @property
    def pawn(self) -> Optional[Address]:
        if self._player_pawn is None:
            match self._init_type:
                case 0:
                    # pawn offset
                    pawn_offset = (
                        self.controller.copy()
                        .offset(CS2.offset.schemas.client_dll.CCSPlayerController.m_hPlayerPawn)
                        .u32()
                    )

                    # list entry
                    pawn_list_entry_address = self._get_list_entry_address(
                        self._entity_list_address, pawn_offset
                    )
                    if not pawn_list_entry_address.address: return None

                    # pawn address
                    player_pawn_address = pawn_list_entry_address.offset(
                        self._get_list_entry_offset(pawn_offset)
                    ).pointer()
                    if not player_pawn_address.address: return None

                    self._player_pawn = player_pawn_address
                case 1: self._player_pawn = self._player_pawn_address
                case _: return None

        return self._player_pawn

    # @property
    # def health(self) -> int:
    #     return (
    #         self.controller.copy()
    #         .offset(CS2.offset.schemas.client_dll.CCSPlayerController.m_iPawnHealth)
    #         .u16()
    #     )

    @property
    def health(self) -> int:
        return (
            self.pawn.copy()
            .offset(CS2.offset.schemas.client_dll.C_BaseEntity.m_iHealth)
            .u16()
        )

    @property
    def pos(self) -> Vec3:
        return (
            self.pawn.copy()
            .offset(CS2.offset.schemas.client_dll.C_BasePlayerPawn.m_vOldOrigin)
            .vec3()
        )

    @property
    def angle(self) -> Vec2:
        return (
            self.pawn.copy()
            .offset(CS2.offset.schemas.client_dll.C_CSPlayerPawnBase.m_angEyeAngles)
            .vec2()
        )

    @property
    def team_num(self) -> int:
        return (
            self.pawn.copy()
            .offset(CS2.offset.schemas.client_dll.C_BaseEntity.m_iTeamNum)
            .u8()
        )

