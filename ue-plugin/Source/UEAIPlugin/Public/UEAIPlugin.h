// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Modules/ModuleManager.h"
#include "Framework/Commands/UICommandList.h"

class FUEAIPluginModule : public IModuleInterface
{
public:
    /** IModuleInterface implementation */
    virtual void StartupModule() override;
    virtual void ShutdownModule() override;

    /** Get the HTTP server URL from config */
    static FString GetBackendServerURL();

    /** Check if backend connection is active */
    static bool IsBackendConnected();

    /** Plugin command list */
    static TSharedPtr<FUICommandList> PluginCommands;

private:
    /** Register editor extensions */
    void RegisterEditorExtensions();

    /** Unregister editor extensions */
    void UnregisterEditorExtensions();
};
