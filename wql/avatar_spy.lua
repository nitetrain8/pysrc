function(event,prefix,message)
    if prefix == "SB_TAINT_FA" then
        --On engage reset the groups
        if message == "STARTING" then
            aura_env.groups = {
                {},
                {}
            }
        elseif string.gmatch(message,"([^\^]+)") then
            
            --Message is a player guid with the group number e.g. player-01239i9ad^1
            local msgs ={}
            for piece in string.gmatch(message,"([^\^]+)") do 
                msgs[#msgs+1]=piece 
            end
            name = select(6, GetPlayerInfoByGUID(msgs[1]))            
            aura_env.groups[tonumber(msgs[2])][#aura_env.groups[tonumber(msgs[2])]+1] = {name= name, duration= ""}
        end        
    end
end


function()
    if WeakAuras.IsOptionsOpen() then
        return "Tainted Essence Tracker\nSome mong 1 - 6\nSome mong 2 - 6\nSome mong 3 - 6\nSome mong 3 - 6\nSome mong 3 - 6\n"
    end
    
    if aura_env.last and  aura_env.display and GetTime() - aura_env.last < 0.3 then
        return aura_env.display
    end
    
    aura_env.last = GetTime()
    
    local display = 'Right Group:\n'
    local e = aura_env
    for _, group in pairs(aura_env.groups) do
        display = display .. "\nLeft Group: \n"
        for _, player in pairs(group) do        
            
            --Get information about the players debuff
            local _,_,_,stacks,_,_,expires = UnitDebuff(player.name, e.spellInfo) 
            
            --Stacks they have
            player.stacks = stacks or 0
            
            --How long they have left on the debuff
            if expires then
                expires = e.round(expires - GetTime())
            else 
                expires = 0
            end
            
            player.duration = expires
            
            --Check if the player is alive and is actually a unit, incase spelling mistake or something
            if UnitIsDead(player.name) or not UnitExists(player.name) then
                display = display .. "|c996e6e6e" .. e.skullIcon 
                .. player.name .. e.skullIcon .. "|r\n"
                player.dead = true
            else
                --If they are eligble for soaking
                if player.stacks < e.maxStacks then
                    if player.duration > 57 then
                        display = display .. "|c0089ff7c> " .. player.name .. ": " .. player.stacks 
                        .. e.debuffIcon .. player.duration ..  "s <|r\n"
                    else
                        display = display .. player.name .. ": " .. player.stacks .. e.debuffIcon 
                        .. player.duration .. "s\n"
                    end
                else
                    --people who have already soaked
                    display = display .. "|c00ff4551" .. player.name .. ": " .. player.stacks  .. e.debuffIcon 
                    .. player.duration .. "s|r\n"
                end
            end
            
        end
    end

    
    e.display = display
    return display
end

function(event,prefix,message)
    if prefix == "SB_TAINT_FA" then
        --On engage reset the groups
        if message == "STARTING" then
            aura_env.groups = {
                {},
                {}
            }
        elseif message == "FINISHED" then
            for _, group in pairs(aura_env.groups) do
                for _, player in pairs(group) do
                    print(player.name)
                end
                
            end
        elseif string.gmatch(message,"([^\^]+)") then
            
            --Message is a player guid with the group number e.g. player-01239i9ad^1
            local msgs ={}
            for piece in string.gmatch(message,"([^\^]+)") do 
                msgs[#msgs+1]=piece 
            end
            print(message)
            name = select(6, GetPlayerInfoByGUID(msgs[1]))            
            aura_env.groups[tonumber(msgs[2])][#aura_env.groups[tonumber(msgs[2])]+1] = {name= name, duration= ""}
        end        
    end
end

function(event,prefix,message)
    if prefix == "SB_TAINT_FA" then
        --On engage reset the groups
        if message == "STARTING" then
            aura_env.groups = {
                {},
                {}
            }
        elseif message == "FINISHED" then
            --If the current player is found, then set that group as their soaking group
            local playerFound = false
            local players
            
            for _, group in pairs(aura_env.groups) do
                for index, player in pairs(group) do
                    if UnitName("player") == player then
                        playerFound = index
                        players = group
                        break
                    end
                end
            end
            
            if playerFound and players then
                
                aura_env.soakingGroup = {}
                
                for _, player in pairs(players) do               
                    table.insert(aura_env.soakingGroup, {name = player, stacks = "", duration = ""})
                end
                
                --Find out who is the player soaking before them
                if (playerFound - 1) == 0 then
                    --If they are the first soaker then get the last player
                    aura_env.playerBefore = table.getn(aura_env.soakingGroup)
                else
                    aura_env.playerBefore = (playerFound - 1)
                end
                
                aura_env.running = true
            end
        elseif string.gmatch(message,"([^\^]+)") then
            
            --Message is a player guid with the group number e.g. player-01239i9ad^1
            local msgs ={}
            for piece in string.gmatch(message,"([^\^]+)") do 
                msgs[#msgs+1]=piece 
            end
            
            aura_env.groups[tonumber(msgs[2])][#aura_env.groups[tonumber(msgs[2])]+1] = 
            name = select(6, GetPlayerInfoByGUID(msgs[1]))
            
        end        
    end
end

