// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "HttpModule.h"
#include "Interfaces/IHttpRequest.h"
#include "Interfaces/IHttpResponse.h"
#include "Dom/JsonObject.h"
#include "Templates/SharedPointer.h"

DECLARE_LOG_CATEGORY_EXTERN(LogUEAIService, Log, All);

/** Response data from AI service */
USTRUCT(BlueprintType)
struct FUEAIResponse
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite, Category = "AI")
    bool bSuccess = false;

    UPROPERTY(BlueprintReadWrite, Category = "AI")
    FString Content;

    UPROPERTY(BlueprintReadWrite, Category = "AI")
    FString ErrorMessage;

    UPROPERTY(BlueprintReadWrite, Category = "AI")
    float Progress = 0.0f;

    UPROPERTY(BlueprintReadWrite, Category = "AI")
    TArray<FString> Actions;
};

/** Request data to send to AI service */
USTRUCT(BlueprintType)
struct FUEAIRequest
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite, Category = "AI")
    FString UserInput;

    UPROPERTY(BlueprintReadWrite, Category = "AI")
    FString SessionID;

    UPROPERTY(BlueprintReadWrite, Category = "AI")
    TMap<FString, FString> ContextData;
};

/** Service for communicating with the UE AI backend */
class FUEAIService
{
public:
    static FUEAIService& Get();

    /** Initialize the service */
    void Initialize();

    /** Shutdown the service */
    void Shutdown();

    /** Check if connected to backend */
    bool IsConnected() const;

    /** Send a chat request to the backend */
    void SendChatRequest(const FUEAIRequest& Request, TFunction<void(const FUEAIResponse&)> OnComplete);

    /** Send a viewport frame to the backend */
    void SendViewportFrame(const TArray<uint8>& ImageData, int32 Width, int32 Height, TFunction<void(const FUEAIResponse&)> OnComplete);

    /** Generate an asset */
    void GenerateAsset(const FString& Prompt, const FString& AssetType, TFunction<void(const FUEAIResponse&)> OnComplete);

private:
    FUEAIService() = default;

    /** Make HTTP request to backend */
    void MakeRequest(const FString& Endpoint, const TSharedPtr<FJsonObject>& Payload, TFunction<void(const FUEAIResponse&)> OnComplete);

    /** Handle HTTP response */
    void HandleHttpResponse(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful, TFunction<void(const FUEAIResponse&)> OnComplete);

    FString BackendServerURL;
    bool bIsInitialized = false;
    bool bIsConnected = false;
};
