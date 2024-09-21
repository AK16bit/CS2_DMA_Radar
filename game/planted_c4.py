from process.address import Address
from process.cs2 import CS2


class PlantedC4:
    def __init__(self, address: Address):
        self.address = address


    @staticmethod
    def _get_game_time() -> float:
        return CS2.offset.signatures.client.dwGlobalVars.pointer().offset(0x34).float()

    @property
    def is_ticking(self) -> bool:
        return self.address.copy().offset(CS2.offset.schemas.client_dll.C_PlantedC4.m_bBombTicking).bool()

    @property
    def site(self) -> str:
        return ("A", "B", "C")[self.address.copy().offset(CS2.offset.schemas.client_dll.C_PlantedC4.m_nBombSite).i8()]

    @property
    def explode_game_time(self) -> float:
        return self.address.copy().offset(CS2.offset.schemas.client_dll.C_PlantedC4.m_flC4Blow).float()

    @property
    def explode_time_left(self) -> float:
        return self.explode_game_time - self._get_game_time()

    @property
    def is_defusing(self) -> bool:
        return self.address.copy().offset(CS2.offset.schemas.client_dll.C_PlantedC4.m_bBeingDefused).bool()

    @property
    def defuse_game_time(self) -> float:
        return self.address.copy().offset(CS2.offset.schemas.client_dll.C_PlantedC4.m_flDefuseCountDown).float()

    @property
    def defuse_time_length(self) -> float:
        return self.address.copy().offset(CS2.offset.schemas.client_dll.C_PlantedC4.m_flDefuseLength).float()

    @property
    def defuse_time_left(self) -> float:
        return self.defuse_game_time - self._get_game_time()

    @property
    def can_defused(self) -> bool:
        return self.defuse_game_time < self.explode_game_time

    def test(self) -> None:
        print(self.address)
        print("m_bBombTicking: %s, m_flC4Blow: %s, m_bBeingDefused: %s, m_flDefuseLength: %s, m_flDefuseCountDown: %s" % (
            self.address.copy().offset(CS2.offset.schemas.client_dll.C_PlantedC4.m_bBombTicking).bool(),
            self.address.copy().offset(CS2.offset.schemas.client_dll.C_PlantedC4.m_flC4Blow).float(),
            self.address.copy().offset(CS2.offset.schemas.client_dll.C_PlantedC4.m_bBeingDefused).bool(),
            self.address.copy().offset(CS2.offset.schemas.client_dll.C_PlantedC4.m_flDefuseLength).float(),
            self.address.copy().offset(CS2.offset.schemas.client_dll.C_PlantedC4.m_flDefuseCountDown).float(),

        ))