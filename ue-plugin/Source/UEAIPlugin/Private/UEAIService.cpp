// Copyright Epic Games, Inc. All Rights Reserved.

#include "UEAIService.h"
#include "UEAIPluginSettings.h"
#include "Dom/JsonObject.h"
#include "Serialization/JsonSerializer.h"
#include "Serialization/JsonWriter.h"
#include "Misc/ConfigCache.h"
#include "HttpModule.h"

DEFINE_LOG_CATEGORY(LogUEAIService);

FUEAIService& FUEAIService::Get()
{
    static FUEAIService Instance;
    return Instance;
}

void FUEAIService::Initialize()
{
    // Load settings
    UUEAIPluginSettings* Settings = GetMutableDefault<UUEAIPluginSettings>();
    if (Settings)
    {
        BackendServerURL = Settings->BackendServerURL;
    }
    else
    {
        BackendServerURL = TEXT("http://localhost:8000");
    }

    // Initialize HTTP module
    FHttpModule::Get();
    bIsInitialized = true;
    bIsConnected = true;

    UE_LOG(LogUEAIService, Log, TEXT("UE AI Service initialized with backend: %s"), *BackendServerURL);
}

void FUEAIService::Shutdown()
{
    bIsInitialized = false;
    bIsConnected = false;
}

bool FUEAIService::IsConnected() const
{
    return bIsConnected && bIsInitialized;
}

void FUEAIService::SendChatRequest(const FUEAIRequest& Request, TFunction<void(const FUEAIResponse&)> OnComplete)
{
    TSharedPtr<FJsonObject> Payload = MakeShareable(new FJsonObject);

    // Convert request to JSON
    Payload->SetStringField(TEXT("user_input"), Request.UserInput);
    Payload->SetStringField(TEXT("session_id"), Request.SessionID);

    if (Request.ContextData.Num() > 0)
    {
        TSharedPtr<FJsonObject> ContextObj = MakeShareable(new FJsonObject);
        for (const auto& Pair : Request.ContextData)
        {
            ContextObj->SetStringField(Pair.Key, Pair.Value);
        }
        Payload->SetObjectField(TEXT("context_data"), ContextObj);
    }

    MakeRequest(TEXT("/api/chat"), Payload, OnComplete);
}

void FUEAIService::SendViewportFrame(const TArray<uint8>& ImageData, int32 Width, int32 Height, TFunction<void(const FUEAIResponse&)> OnComplete)
{
    // This will be implemented to send image data
    // For now, send a simple request
    TSharedPtr<FJsonObject> Payload = MakeShareable(new FJsonObject);
    Payload->SetNumberField(TEXT("width"), Width);
    Payload->SetNumberField(TEXT("height"), Height);

    MakeRequest(TEXT("/api/viewport"), Payload, OnComplete);
}

void FUEAIService::GenerateAsset(const FString& Prompt, const FString& AssetType, TFunction<void(const FUEAIResponse&)> OnComplete)
{
    TSharedPtr<FJsonObject> Payload = MakeShareable(new FJsonObject);
    Payload->SetStringField(TEXT("prompt"), Prompt);
    Payload->SetStringField(TEXT("asset_type"), AssetType);

    MakeRequest(TEXT("/api/generate"), Payload, OnComplete);
}

void FUEAIService::MakeRequest(const FString& Endpoint, const TSharedPtr<FJsonObject>& Payload, TFunction<void(const FUEAIResponse&)> OnComplete)
{
    if (!bIsInitialized)
    {
        FUEAIResponse Response;
        Response.bSuccess = false;
        Response.ErrorMessage = TEXT("Service not initialized");
        OnComplete(Response);
        return;
    }

    FString URL = BackendServerURL + Endpoint;

    // Serialize JSON payload
    FString PayloadString;
    TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&PayloadString);
    FJsonSerializer::Serialize(Payload.ToSharedRef(), Writer);

    // Create HTTP request
    FHttpRequestRef HttpRequest = FHttpModule::Get().CreateRequest();
    HttpRequest->SetVerb(TEXT("POST"));
    HttpRequest->SetURL(URL);
    HttpRequest->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
    HttpRequest->SetContentAsString(PayloadString);

    HttpRequest->OnProcessRequestComplete().BindLambda(
        [this, OnComplete](FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful)
        {
            HandleHttpResponse(Request, Response, bWasSuccessful, OnComplete);
        }
    );

    HttpRequest->ProcessRequest();
}

void FUEAIService::HandleHttpResponse(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful, TFunction<void(const FUEAIResponse&)> OnComplete)
{
    FUEAIResponse AIResponse;

    if (!bWasSuccessful || !Response.IsValid())
    {
        AIResponse.bSuccess = false;
        AIResponse.ErrorMessage = TEXT("HTTP request failed");
        OnComplete(AIResponse);
        return;
    }

    int32 ResponseCode = Response->GetResponseCode();
    if (ResponseCode != 200)
    {
        AIResponse.bSuccess = false;
        AIResponse.ErrorMessage = FString::Printf(TEXT("Server returned error code: %d"), ResponseCode);
        OnComplete(AIResponse);
        return;
    }

    // Parse response JSON
    FString ResponseString = Response->GetContentAsString();
    TSharedPtr<FJsonObject> ResponseObj;
    TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(ResponseString);

    if (!FJsonSerializer::Deserialize(Reader, ResponseObj) || !ResponseObj.IsValid())
    {
        AIResponse.bSuccess = false;
        AIResponse.ErrorMessage = TEXT("Failed to parse response JSON");
        OnComplete(AIResponse);
        return;
    }

    // Extract response data
    AIResponse.bSuccess = ResponseObj->GetBoolField(TEXT("success"), false);

    if (AIResponse.bSuccess)
    {
        AIResponse.Content = ResponseObj->GetStringField(TEXT("full_response"));
        AIResponse.Progress = ResponseObj->GetNumberField(TEXT("progress"), 100.0f);
    }
    else
    {
        AIResponse.ErrorMessage = ResponseObj->GetStringField(TEXT("error"));
    }

    OnComplete(AIResponse);
}
