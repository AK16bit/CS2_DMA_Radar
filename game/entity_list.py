from time import time
from typing import Self, Optional, List, Dict

from game.planted_c4 import PlantedC4
from game.player_entity import PlayerEntity
from game.projectile_entity import ProjectileEntity
from game.weapon_entity import WeaponEntity
from process.address import Address
from process.cs2 import CS2


class EntityList:
    entity_list_address: Optional[Address]

    player_entities: List[PlayerEntity] = list()
    weapon_entities: Dict[str, List[WeaponEntity]]
    projectile_entities: Dict[str, List[ProjectileEntity]]

    _index_2_controller_cache: Dict[int, Address] = dict()
    _controller_2_pawn_cache: Dict[int, Address] = dict()

    @classmethod
    def get_entity_from_list_entry(cls, offset: int, auto_next_entry: bool = True) -> Optional[Address]:
        return cls.entity_list_address.copy().pointer_chain(
            0x10 + ((0x08 * ((offset & 0x7FFF) >> 9)) if auto_next_entry else 0),
            0x78 * (offset & 0x1FF)
        )

    # @staticmethod
    # def get_list_entry_address(entity_list_address: Address, offset: int) -> Address:
    #     return entity_list_address.copy().offset(0x10 + 0x08 * ((offset & 0x7FFF) >> 9)).pointer()
    #
    # @staticmethod
    # def get_list_entry_offset(offset: int) -> int:
    #     return 0x78 * (offset & 0x1FF)

    @classmethod
    def update_entity_list_address(cls) -> Self:
        cls.entity_list_address = CS2.offset.signatures.client.dwEntityList.pointer()
        return cls
        # cls.update_player_entity()


    @classmethod
    def update_player_entity(cls, max_player_index: Optional[int | str] = 64) -> Self:
        max_player_index: int
        if max_player_index is None or max_player_index == "auto":
            max_player_index = CS2.offset.signatures.engine2.dwNetworkGameClient.pointer().offset(
                CS2.offset.signatures.engine2.dwNetworkGameClient_maxClients.address
            ).u32()
        elif isinstance(max_player_index, str): raise ValueError
        elif not isinstance(max_player_index, int): raise ValueError

        player_entities = list()
        for entity_index in range(max_player_index):
            player_entity = cls.player_read(entity_index)
            if player_entity is None: continue

            player_entities.append(player_entity)

        cls.player_entities = player_entities
        return cls


    @classmethod
    def update_world_entity(cls, max_entity_index: int = 1024) -> Self:
        weapon_entities = dict()
        projectile_entities = dict()
        for entity_index in range(64, max_entity_index):
            entity_address = EntityList.get_entity_from_list_entry(entity_index, auto_next_entry=False)
            # entity_address = cls.entity_list_address.copy().pointer_chain(0x10, 0x78 * (entity_index & 0x1FF))
            if not entity_address.address: continue

            try: class_name = entity_address.copy().pointer_chain(0x10, 0x20).str(32)
            except Exception: continue
            if class_name is None: continue

            if "weapon" in class_name:
                weapon_entities.setdefault(class_name, list()).append(entity_address)

            if "projectile" in class_name:
                projectile_entities.setdefault(class_name, list()).append(entity_address)
                # print(entity_index, class_name, entity_address)

        cls.weapon_entities = weapon_entities
        cls.projectile_entities = projectile_entities

        # print(time(), cls.projectile_entities)
        return cls

    @classmethod
    def player_read(cls, player_index: int) -> Optional[PlayerEntity]:
        player_entity = PlayerEntity(cls.entity_list_address, player_index)

        if (player_controller_address := cls._index_2_controller_cache.get(player_index, None)) is None:
            if player_entity.controller is None: return None
            cls._index_2_controller_cache.update({player_index: player_entity.controller})
        else:
            player_entity._player_controller = player_controller_address

        if (
        player_pawn_address := cls._controller_2_pawn_cache.get(player_entity.controller.address, None)) is None:
            if player_entity.pawn is None: return None
            cls._controller_2_pawn_cache.update({player_entity.controller.address: player_entity.pawn})
        else:
            player_entity._player_pawn = player_pawn_address

        return player_entity


    @staticmethod
    def planted_c4_read() -> Optional[PlantedC4]:
        game_rule_address: Address = CS2.offset.signatures.client.dwGameRules.pointer()
        is_c4_planted = (
            game_rule_address.copy()
            .offset(CS2.offset.schemas.client_dll.C_CSGameRules.m_bBombPlanted)
            .bool()
        )
        if not is_c4_planted: return None

        planted_c4_address = CS2.offset.signatures.client.dwPlantedC4.pointer().pointer()
        if not planted_c4_address.address: return None

        return PlantedC4(planted_c4_address)



    @classmethod
    def clear_cache(cls) -> None:
        cls._index_2_controller_cache.clear()
        cls._controller_2_pawn_cache.clear()


