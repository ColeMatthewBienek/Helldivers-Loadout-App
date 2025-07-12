#SingleInstance force
SetKeyDelay, 70

^1::
    SendInput {L down}
    SendInput {Down}
    Sleep 70
    SendInput {Left}
    Sleep 70
    SendInput {Right}
    Sleep 70
    SendInput {Up}
    Sleep 70
    SendInput {Down}
    Sleep 70
    SendInput {L up}
    Return

^2::
    SendInput {L down}
    SendInput {Down}
    Sleep 70
    SendInput {Up}
    Sleep 70
    SendInput {Left}
    Sleep 70
    SendInput {Down}
    Sleep 70
    SendInput {Up}
    Sleep 70
    SendInput {Right}
    Sleep 70
    SendInput {Down}
    Sleep 70
    SendInput {Up}
    Sleep 70
    SendInput {L up}
    Return

^3::
    SendInput {L down}
    SendInput {Down}
    Sleep 70
    SendInput {Left}
    Sleep 70
    SendInput {Up}
    Sleep 70
    SendInput {Right}
    Sleep 70
    SendInput {L up}
    Return

^4::
    SendInput {L down}
    SendInput {Up}
    Sleep 70
    SendInput {Right}
    Sleep 70
    SendInput {Down}
    Sleep 70
    SendInput {Right}
    Sleep 70
    SendInput {L up}
    Return
