package com.trademind.astrology.api

import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Body
import retrofit2.http.Path

interface AstrologyApi {
    @GET("/api/v1/mobile/dashboard")
    suspend fun getDashboard(): DashboardResponse

    @POST("/api/v1/mobile/charts")
    suspend fun createChart(@Body request: ChartRequest): CreateChartResponse

    @POST("/api/v1/mobile/compatibility")
    suspend fun getCompatibility(@Body request: CompatibilityRequest): CompatibilityResponse

    @GET("/api/v1/predict/explain/{domain}")
    suspend fun explainPrediction(@Path("domain") domain: String): ExplanationResponse

    @POST("/api/tracking/outcome")
    suspend fun reportOutcome(@Body outcome: OutcomeRequest): BaseResponse

    @GET("/api/tracking/history")
    suspend fun getMatchRate(): MatchRateResponse

    @GET("/api/v1/mobile/muhurta")
    suspend fun getMuhurta(): MuhurtaResponse
}

data class DashboardResponse(
    val preds: PredictionData,
    val daily: DailyForecast,
    val remedies: List<Remedy>,
    val planets: List<PlanetUiData>?,
    val divisional_charts: Map<String, Map<String, Int>>?,
    val chara_dasha: List<String>?,
    val bazi_pillars: List<String>?,
    val hellenistic_releasing: String?,
    val gene_keys_profile: String?,
    val ashtakavarga: Map<String, Any>?,
    val pratyantar_dasha: List<DashaPeriod>?,
    val bhava_bala: Map<String, Double>?
)

data class DashaPeriod(
    val lord: String,
    val start: String,
    val end: String,
    val level: Int
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

data class ChartRequest(
    val name: String,
    val dob: String,
    val tob: String,
    val place: String
)

data class CreateChartResponse(
    val status: String,
    val chart_id: String?
)

data class PlanetUiData(
    val name: String,
    val rashi: Int,
    val house: Int,
    val is_retrograde: Boolean,
    val is_combust: Boolean,
    val dignity: String,
    val strength_rupas: Double?,
    val strength_factors: List<String>?,
    val fixed_star_label: String?
)

data class CompatibilityRequest(
    val boy_name: String,
    val boy_dob: String,
    val boy_tob: String,
    val boy_place: String,
    val girl_name: String,
    val girl_dob: String,
    val girl_tob: String,
    val girl_place: String
)

data class CompatibilityResponse(
    val status: String,
    val total_score: Double,
    val max_score: Double,
    val verdict: String,
    val kutas: List<KutaItem>,
    val deep_comparison: Map<String, Any>?
)

data class KutaItem(
    val name: String,
    val score: Double,
    val max: Double,
    val status: String
)

data class MuhurtaResponse(
    val status: String,
    val choghadiya: List<ChoghadiyaPeriod>,
    val brahma_muhurta: TimeRange,
    val abhijit_muhurta: TimeRange
)

data class ChoghadiyaPeriod(
    val name: String,
    val start: String,
    val end: String,
    val is_auspicious: Boolean
)

data class TimeRange(val start: String, val end: String)
