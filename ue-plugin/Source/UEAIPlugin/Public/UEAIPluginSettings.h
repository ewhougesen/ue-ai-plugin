// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Engine/DeveloperSettingsBackedByVariant.h"
#include "UEAIPluginSettings.generated.h"

UCLASS(Config = UEAIPlugin)
class UUEAIPluginSettings : public UDeveloperSettingsBackedByVariant
{
    GENERATED_BODY()

public:
    UUEAIPluginSettings()
    {
        BackendServerURL = TEXT("http://localhost:8000");
        bAutoConnect = true;
        ChatHistoryLimit = 50;
    }

    /** The URL of the backend AI server */
    UPROPERTY(EditAnywhere, Config, Category = "Connection", Meta = (DisplayName = "Backend Server URL"))
    FString BackendServerURL;

    /** Automatically connect to backend on startup */
    UPROPERTY(EditAnywhere, Config, Category = "Connection", Meta = (DisplayName = "Auto Connect"))
    bool bAutoConnect;

    /** Maximum number of chat messages to keep in history */
    UPROPERTY(EditAnywhere, Config, Category = "Chat", Meta = (DisplayName = "Chat History Limit"))
    int32 ChatHistoryLimit;

    /** API key for z.ai (optional, can also use environment) */
    UPROPERTY(EditAnywhere, Config, Category = "Connection", Meta = (DisplayName = "z.ai API Key"))
    FString ZaiAPIKey;
};
