package com.trademind.astrology.api

import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Body
import retrofit2.http.Path

interface AstrologyApi {
    @GET("/dashboard")
    suspend fun getDashboard(): DashboardResponse

    @GET("/api/v1/predict/explain/{domain}")
    suspend fun explainPrediction(@Path("domain") domain: String): ExplanationResponse

    @POST("/api/tracking/outcome")
    suspend fun reportOutcome(@Body outcome: OutcomeRequest): BaseResponse

    @GET("/api/tracking/history")
    suspend fun getMatchRate(): MatchRateResponse
}

data class DashboardResponse(
    val preds: PredictionData,
    val daily: DailyForecast,
    val remedies: List<Remedy>
)

data class PredictionData(
    val predictions: List<DomainPrediction>
)

data class DomainPrediction(
    val domain: String,
    val score: Double,
    val prediction_strength: String,
    val summary: String,
    val supporting_signals: List<String>,
    val conflicting_signals: List<String>,
    val timing_window: TimingWindow
)

data class TimingWindow(
    val start: String?,
    val peak: String?,
    val end: String?,
    val description: String
)

data class DailyForecast(
    val strongest_theme: String,
    val current_dasha: String,
    val opportunities: List<String>
)

data class Remedy(
    val planet: String,
    val action: String,
    val type: String,
    val approach: String,
    val priority: String,
    val why: String
)

data class ExplanationResponse(
    val facts: List<Any>,
    val explanation: Map<String, Any>
)

data class OutcomeRequest(
    val category: String,
    val prediction: String,
    val status: String,
    val notes: String
)

data class BaseResponse(val success: Boolean)

data class MatchRateResponse(
    val stats: MatchStats
)

data class MatchRateStats(
    val personal_accuracy_score: Double,
    val total_tracked: Int
)

// To avoid duplicate naming with the model above
data class MatchStats(
    val personal_accuracy_score: Double,
    val total_tracked: Int
)
