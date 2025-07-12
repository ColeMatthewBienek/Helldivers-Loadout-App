;basic strats
; Updated: 2025-07-11 with Yellow stratagems and explicit key down/up events
#SingleInstance ignore

^5:: ; Reinforce
    Send, {l down}
    Sleep, 50
    Send, {Up down}
    Sleep, 50
    Send, {Up up}
    Sleep, 100
    Send, {Down down}
    Sleep, 50
    Send, {Down up}
    Sleep, 100
    Send, {Right down}
    Sleep, 50
    Send, {Right up}
    Sleep, 100
    Send, {Left down}
    Sleep, 50
    Send, {Left up}
    Sleep, 100
    Send, {Up down}
    Sleep, 50
    Send, {Up up}
    Sleep, 100
    Send, {l up}
    Return

^6:: ; Resupply
    Send, {l down}
    Sleep, 50
    Send, {Down down}
    Sleep, 50
    Send, {Down up}
    Sleep, 100
    Send, {Down down}
    Sleep, 50
    Send, {Down up}
    Sleep, 100
    Send, {Up down}
    Sleep, 50
    Send, {Up up}
    Sleep, 100
    Send, {Right down}
    Sleep, 50
    Send, {Right up}
    Sleep, 100
    Send, {l up}
    Return

^7:: ; Eagle Rearm
    Send, {l down}
    Sleep, 50
    Send, {Up down}
    Sleep, 50
    Send, {Up up}
    Sleep, 100
    Send, {Up down}
    Sleep, 50
    Send, {Up up}
    Sleep, 100
    Send, {Left down}
    Sleep, 50
    Send, {Left up}
    Sleep, 100
    Send, {Right down}
    Sleep, 50
    Send, {Right up}
    Sleep, 100
    Send, {Down down}
    Sleep, 50
    Send, {Down up}
    Sleep, 100
    Send, {Down down}
    Sleep, 50
    Send, {Down up}
    Sleep, 100
    Send, {l up}
    Return

!1:: ; SSSD Delivery
    Send, {l down}
    Sleep, 50
    Send, {Down down}
    Sleep, 50
    Send, {Down up}
    Sleep, 100
    Send, {Down down}
    Sleep, 50
    Send, {Down up}
    Sleep, 100
    Send, {Down down}
    Sleep, 50
    Send, {Down up}
    Sleep, 100
    Send, {Up down}
    Sleep, 50
    Send, {Up up}
    Sleep, 100
    Send, {Up down}
    Sleep, 50
    Send, {Up up}
    Sleep, 100
    Send, {l up}
    Return

!2:: ; Seismic Probe
    Send, {l down}
    Sleep, 50
    Send, {Up down}
    Sleep, 50
    Send, {Up up}
    Sleep, 100
    Send, {Up down}
    Sleep, 50
    Send, {Up up}
    Sleep, 100
    Send, {Left down}
    Sleep, 50
    Send, {Left up}
    Sleep, 100
    Send, {Right down}
    Sleep, 50
    Send, {Right up}
    Sleep, 100
    Send, {Down down}
    Sleep, 50
    Send, {Down up}
    Sleep, 100
    Send, {Down down}
    Sleep, 50
    Send, {Down up}
    Sleep, 100
    Send, {l up}
    Return

!3:: ; Upload Data
    Send, {l down}
    Sleep, 50
    Send, {Up down}
    Sleep, 50
    Send, {Up up}
    Sleep, 100
    Send, {Up down}
    Sleep, 50
    Send, {Up up}
    Sleep, 100
    Send, {Left down}
    Sleep, 50
    Send, {Left up}
    Sleep, 100
    Send, {Right down}
    Sleep, 50
    Send, {Right up}
    Sleep, 100
    Send, {Down down}
    Sleep, 50
    Send, {Down up}
    Sleep, 100
    Send, {Down down}
    Sleep, 50
    Send, {Down up}
    Sleep, 100
    Send, {l up}
    Return

!4:: ; NUX-223 Hellbomb
    Send, {l down}
    Sleep, 50
    Send, {Down down}
    Sleep, 50
    Send, {Down up}
    Sleep, 100
    Send, {Up down}
    Sleep, 50
    Send, {Up up}
    Sleep, 100
    Send, {Left down}
    Sleep, 50
    Send, {Left up}
    Sleep, 100
    Send, {Down down}
    Sleep, 50
    Send, {Down up}
    Sleep, 100
    Send, {Up down}
    Sleep, 50
    Send, {Up up}
    Sleep, 100
    Send, {Right down}
    Sleep, 50
    Send, {Right up}
    Sleep, 100
    Send, {Down down}
    Sleep, 50
    Send, {Down up}
    Sleep, 100
    Send, {Up down}
    Sleep, 50
    Send, {Up up}
    Sleep, 100
    Send, {l up}
    Return

!5:: ; SEAF Artillery
    Send, {l down}
    Sleep, 50
    Send, {Right down}
    Sleep, 50
    Send, {Right up}
    Sleep, 100
    Send, {Up down}
    Sleep, 50
    Send, {Up up}
    Sleep, 100
    Send, {Up down}
    Sleep, 50
    Send, {Up up}
    Sleep, 100
    Send, {Down down}
    Sleep, 50
    Send, {Down up}
    Sleep, 100
    Send, {l up}
    Return

!6:: ; Prospecting Drill
    Send, {l down}
    Sleep, 50
    Send, {Down down}
    Sleep, 50
    Send, {Down up}
    Sleep, 100
    Send, {Down down}
    Sleep, 50
    Send, {Down up}
    Sleep, 100
    Send, {Left down}
    Sleep, 50
    Send, {Left up}
    Sleep, 100
    Send, {Right down}
    Sleep, 50
    Send, {Right up}
    Sleep, 100
    Send, {Down down}
    Sleep, 50
    Send, {Down up}
    Sleep, 100
    Send, {Down down}
    Sleep, 50
    Send, {Down up}
    Sleep, 100
    Send, {l up}
    Return

!7:: ; Tectonic Drill
    Send, {l down}
    Sleep, 50
    Send, {Down down}
    Sleep, 50
    Send, {Down up}
    Sleep, 100
    Send, {Left down}
    Sleep, 50
    Send, {Left up}
    Sleep, 100
    Send, {Up down}
    Sleep, 50
    Send, {Up up}
    Sleep, 100
    Send, {Down down}
    Sleep, 50
    Send, {Down up}
    Sleep, 100
    Send, {Right down}
    Sleep, 50
    Send, {Right up}
    Sleep, 100
    Send, {l up}
    Return