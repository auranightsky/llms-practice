import copy
import json

from langchain.tools import tool

from src.agent.speaker_state import DEFAULT_SPEAKER_STATE


def create_speaker_tools(retriever, speaker_state):
    """
    Create speaker tools.

    retriever:
        The RAG retriever built from the speaker manual.

    speaker_state:
        The dictionary containing the simulated speaker settings.
    """

    service_ticket_counter = [1000]

    @tool
    def search_manual(query: str) -> str:
        """스피커 매뉴얼에서 질문과 관련된 정보를 검색합니다."""

        print("\nTOOL: search_manual()")

        docs = retriever.invoke(query)

        if not docs:
            return "매뉴얼에서 관련 내용을 찾지 못했습니다."

        results = []

        for i, doc in enumerate(docs, start=1):
            page = doc.metadata.get("page", "unknown")

            results.append(
                f"[검색 결과 {i} / 페이지 {page}]\n"
                f"{doc.page_content}"
            )

        return "\n\n".join(results)

    @tool
    def get_speaker_status() -> str:
        """현재 스피커의 전원과 설정 상태를 확인합니다."""

        print("\nTOOL: get_speaker_status()")

        return json.dumps(
            speaker_state,
            ensure_ascii=False,
            indent=2,
        )

    @tool
    def change_speaker_setting(
        setting: str,
        value: str,
    ) -> str:
        """
        스피커 설정을 변경합니다.

        setting:
            volume, muted, microphone, night_mode, sound_mode 또는 power.

        value:
            변경할 값. 숫자 설정도 문자열로 전달합니다.
        """

        print(
            "\nTOOL: change_speaker_setting("
            f"setting={setting!r}, value={value!r})"
        )

        setting = setting.strip().lower()
        value = value.strip().lower()

        boolean_settings = {
            "power",
            "muted",
            "microphone",
            "night_mode",
        }

        if setting in boolean_settings:
            if value in {"true", "on", "yes", "1", "켜기", "켜", "예"}:
                new_value = True
            elif value in {
                "false", "off", "no", "0", "끄기", "꺼", "아니오"
            }:
                new_value = False
            else:
                return (
                    f"{setting} 값은 on/off 또는 true/false로 "
                    "입력해야 합니다."
                )

            speaker_state[setting] = new_value

            if setting == "microphone":
                speaker_state["led"] = (
                    "white" if new_value else "red"
                )

            return (
                f"{setting} 설정을 "
                f"{'켜짐' if new_value else '꺼짐'}으로 변경했습니다."
            )

        if setting == "volume":
            try:
                new_volume = int(value)
            except ValueError:
                return "음량은 0부터 100 사이의 정수여야 합니다."

            if not 0 <= new_volume <= 100:
                return "음량은 0부터 100 사이여야 합니다."

            speaker_state["volume"] = new_volume

            return f"음량을 {new_volume}으로 변경했습니다."

        if setting == "sound_mode":
            allowed_modes = {
                "standard",
                "music",
                "ai_sound",
            }

            if value not in allowed_modes:
                return (
                    "sound_mode는 standard, music, ai_sound 중 "
                    "하나여야 합니다."
                )

            speaker_state["sound_mode"] = value

            return f"사운드 모드를 {value}로 변경했습니다."

        return (
            f"지원하지 않는 설정입니다: {setting}. "
            "지원 설정: power, volume, muted, microphone, "
            "night_mode, sound_mode."
        )

    @tool
    def disconnect_bluetooth() -> str:
        """현재 연결된 블루투스 기기의 연결을 해제합니다."""

        print("\nTOOL: disconnect_bluetooth()")

        if not speaker_state["bluetooth_connected"]:
            return "현재 연결된 블루투스 기기가 없습니다."

        old_device = speaker_state["connected_bluetooth_device"]

        speaker_state["bluetooth_connected"] = False
        speaker_state["connected_bluetooth_device"] = None

        return (
            f"기존 블루투스 기기({old_device})의 연결을 해제했습니다."
        )

    @tool
    def enter_pairing_mode() -> str:
        """새 블루투스 기기와 연결할 수 있도록 페어링 모드로 전환합니다."""

        print("\nTOOL: enter_pairing_mode()")

        if speaker_state["bluetooth_connected"]:
            return (
                "현재 다른 블루투스 기기가 연결되어 있습니다. "
                "먼저 disconnect_bluetooth를 사용하세요."
            )

        speaker_state["pairing_mode"] = True
        speaker_state["led"] = "red -> green -> blue blinking"

        return (
            "스피커를 Bluetooth 페어링 모드로 변경했습니다. "
            "실제 기기를 연결하는 기능은 구현되어 있지 않습니다."
        )

    @tool
    def reset_speaker(approved: bool, reason: str) -> str:
        """
        스피커 설정을 공장 초기화합니다.

        approved:
            사용자가 초기화에 명시적으로 동의했을 때만 True로 설정합니다.

        reason:
            초기화가 필요한 이유.
        """

        print("\nTOOL: reset_speaker()")

        if not approved:
            return (
                "초기화가 실행되지 않았습니다. "
                "사용자의 명시적인 승인이 필요합니다."
            )

        speaker_state.clear()
        speaker_state.update(
            copy.deepcopy(DEFAULT_SPEAKER_STATE)
        )

        return (
            "사용자 승인을 받아 스피커의 Mock 상태를 "
            f"초기화했습니다. 이유: {reason}"
        )

    @tool
    def request_service(
        problem: str,
        attempted_actions: str = "",
    ) -> str:
        """
        문제 해결이 되지 않았을 때 교육용 서비스 요청을 생성합니다.

        problem:
            해결되지 않은 문제.

        attempted_actions:
            이미 시도한 해결 방법.
        """

        print("\nTOOL: request_service()")

        service_ticket_counter[0] += 1
        ticket_id = f"DEMO-{service_ticket_counter[0]}"

        speaker_state["needs_service"] = True

        return (
            "교육용 서비스 요청이 생성되었습니다.\n"
            f"- Ticket: {ticket_id}\n"
            f"- 문제: {problem}\n"
            f"- 시도한 조치: {attempted_actions or '기록 없음'}"
        )

    return [
        search_manual,
        get_speaker_status,
        change_speaker_setting,
        disconnect_bluetooth,
        enter_pairing_mode,
        reset_speaker,
        request_service,
    ]