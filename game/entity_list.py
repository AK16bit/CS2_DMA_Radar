from typing import Self, Optional, List, Dict

from game.player_entity import PlayerEntity
from process.address import Address
from process.cs2 import CS2


class EntityList:
    entity_list_address: Optional[Address]
    player_entities: Optional[List[PlayerEntity]]

    _index_2_controller_cache: Dict[int, Address] = dict()
    _controller_2_pawn_cache: Dict[int, Address] = dict()


    @classmethod
    def update(cls, max_player_index: Optional[int | str] = 64) -> Self:
        max_player_index: int
        if max_player_index is None or max_player_index == "auto":
            max_player_index = CS2.offset.signatures.engine2.dwNetworkGameClient.pointer().offset(
                CS2.offset.signatures.engine2.dwNetworkGameClient_maxClients.address
            ).u32()
        elif isinstance(max_player_index, str): raise ValueError
        elif not isinstance(max_player_index, int): raise ValueError

        player_entities = list()
        cls.entity_list_address = CS2.offset.signatures.client.dwEntityList.pointer()
        for entity_index in range(max_player_index):
            player_entity = cls.player_read(entity_index)
            if player_entity is None: continue

            player_entities.append(player_entity)
        cls.player_entities = player_entities

        return cls


    @classmethod
    def player_read(cls, player_index: int) -> Optional[PlayerEntity]:
        player_entity = PlayerEntity(cls.entity_list_address, player_index)

        if (player_controller_address := cls._index_2_controller_cache.get(player_index, None)) is None:
            if player_entity.controller is None: return None
            cls._index_2_controller_cache.update({player_index: player_entity.controller})
        else: player_entity._player_controller = player_controller_address

        if (player_pawn_address := cls._controller_2_pawn_cache.get(player_entity.controller.address, None)) is None:
            if player_entity.pawn is None: return None
            cls._controller_2_pawn_cache.update({player_entity.controller.address: player_entity.pawn})
        else: player_entity._player_pawn = player_pawn_address

        return player_entity

    @classmethod
    def clear_cache(cls) -> None:
        cls._index_2_controller_cache = dict()
        cls._controller_2_pawn_cache = dict()

