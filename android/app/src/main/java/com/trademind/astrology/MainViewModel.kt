package com.trademind.astrology

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.trademind.astrology.api.*
import kotlinx.coroutines.launch
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

class MainViewModel : ViewModel() {
    private val retrofit = Retrofit.Builder()
        .baseUrl("http://10.0.2.2:5001") // Standard Android emulator loopback to host
        .addConverterFactory(GsonConverterFactory.create())
        .build()

    private val api = retrofit.create(AstrologyApi::class.java)

    var dashboardData by mutableStateOf<DashboardResponse?>(null)
    var isLoading by mutableStateOf(false)
    var error by mutableStateOf<String?>(null)
    
    // Navigation state (Phase 8 P1)
    var currentScreen by mutableStateOf<Screen>(Screen.BirthProfile)
    
    var selectedExplanation by mutableStateOf<ExplanationResponse?>(null)

    fun calculateChart(name: String, dob: String, tob: String, place: String, confidence: String) {
        viewModelScope.launch {
            isLoading = true
            error = null
            try {
                dashboardData = api.getDashboard()
                currentScreen = Screen.Dashboard
            } catch (e: Exception) {
                error = "Astrological calculation service unavailable."
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
    
    fun refresh() {
        calculateChart("", "", "", "", "")
    }
}
