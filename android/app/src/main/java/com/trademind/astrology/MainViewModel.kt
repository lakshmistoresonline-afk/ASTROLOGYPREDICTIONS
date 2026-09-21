package com.trademind.astrology

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.trademind.astrology.api.*
import kotlinx.coroutines.launch
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

class MainViewModel : ViewModel() {
    private val client = OkHttpClient.Builder().addInterceptor { chain ->
        val newRequest = chain.request().newBuilder()
            .addHeader("Authorization", "Bearer mock_token_native_app")
            .build()
        chain.proceed(newRequest)
    }.build()

    private val retrofit = Retrofit.Builder()
        .baseUrl("http://10.0.2.2:5001") // Standard Android emulator loopback to host
        .client(client)
        .addConverterFactory(GsonConverterFactory.create())
        .build()

    private val api = retrofit.create(AstrologyApi::class.java)

    var dashboardData by mutableStateOf<DashboardResponse?>(null)
    var isLoading by mutableStateOf(false)
    var error by mutableStateOf<String?>(null)
    
    // MVI State Flow Infrastructure
    private val _uiState = kotlinx.coroutines.flow.MutableStateFlow<DashboardUiState>(DashboardUiState.Idle)
    val uiState = _uiState.asStateFlow()

    // Navigation state (Phase 8 P1)
    var currentScreen by mutableStateOf<Screen>(Screen.Login)
    
    var selectedExplanation by mutableStateOf<ExplanationResponse?>(null)

    var compatibilityData by mutableStateOf<CompatibilityResponse?>(null)
    var isCompatibilityLoading by mutableStateOf(false)
    var compatibilityError by mutableStateOf<String?>(null)

    var muhurtaData by mutableStateOf<MuhurtaResponse?>(null)
    var isMuhurtaLoading by mutableStateOf(false)

    var selectedPlanetForInspection by mutableStateOf<PlanetUiData?>(null)

    fun fetchMuhurta() {
        viewModelScope.launch {
            isMuhurtaLoading = true
            try {
                muhurtaData = api.getMuhurta()
            } catch (e: Exception) {}
            finally { isMuhurtaLoading = false }
        }
    }

    fun calculateChart(name: String, dob: String, tob: String, place: String, confidence: String) {
        viewModelScope.launch {
            isLoading = true
            error = null
            _uiState.value = DashboardUiState.Loading
            try {
                val res = api.createChart(ChartRequest(name, dob, tob, place))
                if (res.status == "success") {
                    val dash = api.getDashboard()
                    dashboardData = dash
                    _uiState.value = DashboardUiState.Success(dash)
                    currentScreen = Screen.Dashboard
                } else {
                    error = "Failed to create birth profile."
                    _uiState.value = DashboardUiState.Error("Failed to create profile")
                }
            } catch (e: Exception) {
                error = "Astrological calculation service unavailable: ${e.message}"
                _uiState.value = DashboardUiState.Error(e.message ?: "Unreachable")
            } finally {
                isLoading = false
            }
        }
    }

    fun fetchExplanation(domain: String) {
        viewModelScope.launch {
            isLoading = true
            try {
                selectedExplanation = api.explainPrediction(domain)
                currentScreen = Screen.PredictionDetail(domain)
            } catch (e: Exception) {
                error = "Failed to fetch prediction evidence."
            } finally {
                isLoading = false
            }
        }
    }

    fun reportOutcome(domain: String, prediction: String, status: String) {
        viewModelScope.launch {
            try {
                api.reportOutcome(OutcomeRequest(domain, prediction, status, ""))
            } catch (e: Exception) {
                // Background report failure is non-blocking
            }
        }
    }

    fun calculateCompatibility(bName: String, bDob: String, bPlace: String, gName: String, gDob: String, gPlace: String) {
        viewModelScope.launch {
            isCompatibilityLoading = true
            compatibilityError = null
            try {
                val req = CompatibilityRequest(bName, bDob, "12:00", bPlace, gName, gDob, "12:00", gPlace)
                val response = api.getCompatibility(req)
                if (response.status == "success") {
                    compatibilityData = response
                } else {
                    compatibilityError = "Failed to calculate compatibility match."
                }
            } catch (e: Exception) {
                compatibilityError = "Compatibility engine unreachable: ${e.message}"
            } finally {
                isCompatibilityLoading = false
            }
        }
    }
    
    fun refresh() {
        if (dashboardData != null) {
            viewModelScope.launch {
                try {
                    dashboardData = api.getDashboard()
                } catch (e: Exception) {
                    // non-blocking
                }
            }
        }
    }
}

sealed interface DashboardUiState {
    object Idle : DashboardUiState
    object Loading : DashboardUiState
    data class Success(val data: DashboardResponse) : DashboardUiState
    data class Error(val message: String) : DashboardUiState
}
