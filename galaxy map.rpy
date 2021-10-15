init -1 python: # These are holding figures for screens
    gm_bg = "Map/cera.jpg"
    gm_info = "Map/occupiedcera_info.png"
    GM_selected = None
    if not hasattr(store,'supress_missions'): store.supress_missions = [] # This can be used with after_load_funcs, to add to it, putting the mission jump location in, stops it showing on the map.
                                                                          # Mostly useful for missions that only have a missionx compleate variable in the original story stuff.

init 5 python:
    # Add missions to planets

    # TYDARIA
    TYDARIA.missions.append(["MetAsaga == False and mission2_complete == False", _("Main: Repair and Resupply"), "Tydaria_jump1"])
    TYDARIA.missions.append(["mission_pirateattack == True and mission5_complete == False", _("Main: Attack Pirate Nest"), "piratebaseattack"])
    TYDARIA.missions.append(["tydaria_morepirates == True and mission13_complete == False", _("Side: Annihilate pirate bases"), "clearoutpirates"])
    TYDARIA.missions.append(["tydaria_escort == True", _("Side: Escort civilian freighter"), "jumptotydariaescort"])

    # ASTRAL EXPANSE
    ASTRAL_EXPANSE.missions.append(["mission_pirateattack == True and mission3_complete == False and mission4_complete == False", _("Side: Stop slavers"),"humantraffickers"])

    # PACT STATION
    PACT_STATION.missions.append(["mission_pirateattack == True and mission3_complete == False and mission4_complete == False", _("Side: Destroy PACT outpost"), "pactstationattack"])
    
    # VERSTA
    VERSTA.missions.append(["amissionforalliance == True and mission6_complete == False", _("Main: Rescue Diplomats"), "jumphotversta"])
    VERSTA.missions.append(["versta_ambush == True and mission15_complete == False", _("Side: Ambush Resupply Stations"), "ambushpactresupply"])

    # NOMODORN CORRIDOR
    NOMODORN.missions.append(["missionforryuvia == True and mission9_complete == False", _("Main: Find Crown Jewel"), "jumptonomodorn"])

    # FAR PORT
    FAR_PORT.missions.append(["farport_losttech == True and mission14_complete == False", _("Side: Investigate lost technology"), "investigatemoon"])

    # ONGESS
    ONGESS.missions.append(["greytour == True and mission16_complete == False", _("Main: Meet Admiral Grey"), "arrivalatongess"])

screen galaxymap_buttons: ###################################GALAXY MAP BUTTONS
# Now, picked planets are set to GM_selected so they can be traced by screen code
# Planets have .missions attribute that can be used to set missions to appear.
# A default setting will let planets gen their own mission select options

    modal True
    tag galaxy_map
    
    key "mousedown_4" action NullAction()

    for planet in planets:
        $mod_planet_icon = False
        if planet.shouldShowOnMap():

            $idle_image = "Map/map_icon_base.png"
            $hover_image = "Map/map_icon_hover.png"
            $planet_active = False

            if planet.missions != []:
                for item in planet.missions:
                    if eval(item[0]) and item[2] not in supress_missions:
                        #if len(item) > 3:
                            #if item[3] != []:
                                #$mod_planet_icon = item[3]
                        $planet_active = True
                
            if planet_active:
                $idle_image = "Map/map_icon_base_highlight.png"
                $hover_image = "Map/map_icon_hover_highlight.png"
                if mod_planet_icon != False:
                    $ mod_planet_icon(planet)
                    $ idle_image = gal_icon1
                    $ idle_image = gal_icon2
            
            imagebutton:
                action [SetVariable("GM_selected",planet),Jump(planet.jumpLocation)]
                idle idle_image
                hover hover_image
                xpos planet.xPos ypos planet.yPos
            text planet.name xpos planet.xPos + 55 ypos planet.yPos size 15

    imagebutton:
        xpos 1600 ypos 950
        action Jump("galaxymapend")
        idle "Map/back_button_base.png"
        hover "Map/back_button_hover.png"

label setGMBG:
    if GM_selected != None:
        $gm_bg = GM_selected.background
        $gm_info = GM_selected.info
        image gm_bg:
            gm_bg
        image gm_info:
            gm_info
        $infocard = GM_selected.info
    return
    
label Dynamic_mission:
    call setGMBG from _call_setGMBG
    $ infocard = GM_selected.info
    $ map_back = "Dynamic_Back"

    scene bg black
    show galaxymap:
        alpha 1 zoom 1
        parallel:
            ease 0.5 alpha 0
        parallel:
            ease 1 xpos GM_selected.xPos*-10 ypos GM_selected.yPos*-10 zoom 10
    show gm_bg:
        zoom 0.0268041237113402
        xpos 1297 ypos 480 alpha 0
        parallel:
            ease 1 alpha 1
        parallel:
            ease 0.75 zoom 1 xpos 0 ypos -430
    pause 1
    call screen map_travelto_dynamic
    with dissolve
    
label Dynamic_Back:
    hide gm_info
    scene bg black
    show gm_bg:
        zoom 1
        xpos 0 ypos -430 alpha 1
        parallel:
            ease 0.5 alpha 0
        parallel:
            ease 1 zoom 0.0268041237113402 xpos GM_selected.xPos ypos GM_selected.yPos
    show galaxymap:
        xpos -10*GM_selected.xPos ypos -10*GM_selected.yPos zoom 10 alpha 0
        parallel:
            ease 1.1 alpha 1
        parallel:
            ease 1 xpos 0 ypos 0 zoom 1
    pause 1
    call screen galaxymap_buttons
            
screen map_travelto_dynamic:
    frame:
        xmaximum 900
        xpos 1098
        ypos 620
        background None
        add infocard:
            xpos 0 ypos -450
        vbox:
            spacing -22

            if GM_selected.missions != []:
                $counter = 0
                for mission in GM_selected.missions:
                    if eval(mission[0]) and mission[2] not in supress_missions:
                        $counter += 1
                        if not counter > 4:
                            imagebutton:
                                ypos -35
                                action Jump(mission[2])
                                idle "Map/whitebutton.png"
                                hover "Map/whitebutton_hover.png"
                            text mission[1]:
                                xpos -10 ypos -70
                                font "Font/sui generis rg.ttf" size 27 first_indent 30 line_spacing 10 outlines [ (2, "#000", 0, 0) ]
            imagebutton:
                ypos -35
                action Jump(map_back)
                idle "Map/back_button_base.png"
                hover "Map/back_button_hover.png"
        
label galaxymap:

    window hide
    hide screen ship_map
    show galaxymap
    with dissolve
    $ ship_music = renpy.music.get_playing("music")
    play music "Music/Star_of_Bethlehem.ogg" fadeout 1.5

    call screen galaxymap_buttons

label galaxymapend:

    hide galaxymap
    play music ship_music fadeout 1.5
    $ ship_music = None
    jump dispatch
