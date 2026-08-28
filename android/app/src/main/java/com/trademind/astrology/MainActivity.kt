package com.trademind.astrology

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.trademind.astrology.api.DomainPrediction
import com.trademind.astrology.api.DashboardResponse

class MainActivity : ComponentActivity() {
    private val viewModel: MainViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                Surface(modifier = Modifier.fillMaxSize(), color = Color(0xFF0F172A)) {
                    val currentScreen = viewModel.currentScreen
                    when (currentScreen) {
                        is Screen.BirthProfile -> BirthProfileScreen(viewModel)
                        is Screen.Dashboard -> DashboardScreen(viewModel)
                        is Screen.PredictionDetail -> PredictionDetailScreen(viewModel, currentScreen.domain)
                    }
                }
            }
        }
    }
}

sealed class Screen {
    object BirthProfile : Screen()
    object Dashboard : Screen()
    data class PredictionDetail(val domain: String) : Screen()
}

@Composable
fun BirthProfileScreen(viewModel: MainViewModel) {
    var name by remember { mutableStateOf("") }
    var dob by remember { mutableStateOf("") }
    var tob by remember { mutableStateOf("") }
    var place by remember { mutableStateOf("") }
    var confidence by remember { mutableStateOf("HIGH") }

    Column(
        modifier = Modifier.fillMaxSize().padding(32.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("Create Birth Profile", fontSize = 24.sp, fontWeight = FontWeight.Black, color = Color.White)
        Spacer(modifier = Modifier.height(24.dp))
        
        OutlinedTextField(value = name, onValueChange = { name = it }, label = { Text("Name") }, modifier = Modifier.fillMaxWidth())
        Spacer(modifier = Modifier.height(16.dp))
        OutlinedTextField(value = dob, onValueChange = { dob = it }, label = { Text("Date (YYYY-MM-DD)") }, modifier = Modifier.fillMaxWidth())
        Spacer(modifier = Modifier.height(16.dp))
        OutlinedTextField(value = tob, onValueChange = { tob = it }, label = { Text("Time (HH:MM)") }, modifier = Modifier.fillMaxWidth())
        Spacer(modifier = Modifier.height(16.dp))
        OutlinedTextField(value = place, onValueChange = { place = it }, label = { Text("Birth Place") }, modifier = Modifier.fillMaxWidth())
        Spacer(modifier = Modifier.height(16.dp))
        
        Text("Birth-Time Confidence", fontSize = 12.sp, color = Color.Gray)
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            listOf("HIGH", "MEDIUM", "LOW").forEach { conf ->
                FilterChip(
                    selected = confidence == conf,
                    onClick = { confidence = conf },
                    label = { Text(conf) }
                )
            }
        }

        Spacer(modifier = Modifier.height(32.dp))
        Button(
            onClick = { viewModel.calculateChart(name, dob, tob, place, confidence) },
            modifier = Modifier.fillMaxWidth(),
            enabled = name.isNotBlank() && dob.isNotBlank() && tob.isNotBlank(),
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFFBBF24))
        ) {
            Text("CALCULATE BLUEPRINT", color = Color.Black, fontWeight = FontWeight.Black)
        }
    }
}

@Composable
fun DashboardScreen(viewModel: MainViewModel) {
    val data = viewModel.dashboardData
    val error = viewModel.error

    if (error != null) {
        ErrorScreen(error)
        return
    }

    if (data == null) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            CircularProgressIndicator(color = Color(0xFFFBBF24))
        }
        return
    }

    LazyColumn(
        modifier = Modifier.fillMaxSize().padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        item {
            Header()
        }

        item {
            CurrentDashaCard(data.daily.current_dasha, data.daily.strongest_theme)
        }

        item {
            SectionHeader("CORROBORATED PREDICTIONS")
        }

        items(data.preds.predictions) { pred ->
            PredictionCard(
                pred, 
                onReport = { status -> viewModel.reportOutcome(pred.domain, pred.summary, status) },
                onWhy = { viewModel.fetchExplanation(pred.domain) }
            )
        }

        item {
            SectionHeader("PRIORITY REMEDIES")
        }

        items(data.remedies) { remedy ->
            RemedyCard(remedy.planet, remedy.approach, remedy.why)
        }
    }
}

@Composable
fun ErrorScreen(message: String) {
    Column(
        modifier = Modifier.fillMaxSize().padding(32.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("System Unavailable", fontSize = 20.sp, fontWeight = FontWeight.Black, color = Color.Red)
        Spacer(modifier = Modifier.height(16.dp))
        Text(message, fontSize = 14.sp, color = Color.White, textAlign = androidx.compose.ui.text.style.TextAlign.Center)
    }
}

@Composable
fun Header() {
    Column {
        Text("Namaste", fontSize = 24.sp, fontWeight = FontWeight.Black, color = Color.White)
        Text("JYOTISH OS V1.0.0", fontSize = 12.sp, color = Color(0xFFFBBF24), letterSpacing = 2.sp)
    }
}

@Composable
fun CurrentDashaCard(period: String, theme: String) {
    Box(
        modifier = Modifier.fillMaxWidth()
            .background(brush = Brush.horizontalGradient(listOf(Color(0xFFFBBF24), Color(0xFFF59E0B))), shape = RoundedCornerShape(24.dp))
            .padding(24.dp)
    ) {
        Column {
            Text("CURRENT LIFE PERIOD", fontSize = 10.sp, fontWeight = FontWeight.Black, color = Color.Black.copy(alpha = 0.6f))
            Text(period, fontSize = 28.sp, fontWeight = FontWeight.Black, color = Color.Black)
            Text("Focus: $theme", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.Black)
        }
    }
}

@Composable
fun SectionHeader(title: String) {
    Text(text = title, fontSize = 12.sp, fontWeight = FontWeight.Black, color = Color.Gray, letterSpacing = 1.sp)
}

@Composable
fun PredictionCard(pred: DomainPrediction, onReport: (String) -> Unit, onWhy: () -> Unit) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = Color(0xFF1E293B)),
        shape = RoundedCornerShape(24.dp)
    ) {
        Column(modifier = Modifier.padding(24.dp)) {
            Row(horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
                Text(pred.domain, fontWeight = FontWeight.Bold, color = Color.White)
                Text(pred.prediction_strength, color = Color(0xFFFBBF24), fontWeight = FontWeight.Black, fontSize = 12.sp)
            }
            Spacer(modifier = Modifier.height(8.dp))
            Text(pred.summary, fontSize = 14.sp, color = Color.White.copy(alpha = 0.7f))
            Spacer(modifier = Modifier.height(16.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("PEAK: ", fontSize = 10.sp, fontWeight = FontWeight.Black, color = Color.Gray)
                Text(pred.timing_window.peak ?: "N/A", fontSize = 10.sp, fontWeight = FontWeight.Black, color = Color.White)
                Spacer(modifier = Modifier.weight(1f))
                TextButton(onClick = onWhy) {
                    Text("WHY?", fontSize = 12.sp, color = Color(0xFFFBBF24), fontWeight = FontWeight.Black)
                }
                
                var showOutcomeMenu by remember { mutableStateOf(false) }
                Box {
                    TextButton(onClick = { showOutcomeMenu = true }) {
                        Text("REPORT", fontSize = 10.sp, color = Color.Gray)
                    }
                    DropdownMenu(expanded = showOutcomeMenu, onDismissRequest = { showOutcomeMenu = false }) {
                        listOf("OCCURRED", "PARTIAL", "DID NOT OCCUR").forEach { status ->
                            DropdownMenuItem(
                                text = { Text(status) },
                                onClick = {
                                    onReport(status)
                                    showOutcomeMenu = false
                                }
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun PredictionDetailScreen(viewModel: MainViewModel, domain: String) {
    val explanation = viewModel.selectedExplanation

    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            IconButton(onClick = { viewModel.currentScreen = Screen.Dashboard }) {
                Text("<", color = Color.White, fontSize = 24.sp)
            }
            Text("Deep Evidence: $domain", fontSize = 18.sp, fontWeight = FontWeight.Black, color = Color.White)
        }

        if (explanation == null) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                CircularProgressIndicator()
            }
            return
        }

        LazyColumn(verticalArrangement = Arrangement.spacedBy(12.dp), modifier = Modifier.padding(top = 24.dp)) {
            item {
                Text("DETERMINISTIC EVIDENCE CHAIN", fontSize = 12.sp, fontWeight = FontWeight.Black, color = Color.Gray, letterSpacing = 1.sp)
            }

            val whyList = explanation.explanation["why"] as? List<*>
            whyList?.forEach { item ->
                item {
                    Card(
                        modifier = Modifier.fillMaxWidth(),
                        colors = CardDefaults.cardColors(containerColor = Color(0xFF1E293B)),
                        shape = RoundedCornerShape(16.dp)
                    ) {
                        Text(
                            text = item.toString(),
                            modifier = Modifier.padding(16.dp),
                            color = Color.White.copy(alpha = 0.8f),
                            fontSize = 14.sp
                        )
                    }
                }
            }
            
            item {
                Spacer(modifier = Modifier.height(24.dp))
                Text("PRACTICAL GUIDANCE", fontSize = 12.sp, fontWeight = FontWeight.Black, color = Color.Gray, letterSpacing = 1.sp)
            }
            
            val guide = explanation.explanation["practicalGuidance"] as? List<*>
            guide?.forEach { item ->
                item {
                    Text("• ${item.toString()}", color = Color(0xFFFBBF24), fontSize = 14.sp, modifier = Modifier.padding(horizontal = 8.dp))
                }
            }
        }
    }
}

@Composable
fun RemedyCard(planet: String, approach: String, why: String) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = Color(0xFFFEF3C7).copy(alpha = 0.1f)),
        shape = RoundedCornerShape(24.dp)
    ) {
        Column(modifier = Modifier.padding(24.dp)) {
            Text("$planet ($approach)", fontWeight = FontWeight.Bold, color = Color(0xFFFBBF24))
            Text(why, fontSize = 12.sp, color = Color.White.copy(alpha = 0.5f))
            Spacer(modifier = Modifier.height(12.dp))
            Button(
                onClick = {}, 
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFFBBF24)),
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(12.dp)
            ) {
                Text("COMPLETE REMEDY", color = Color.Black, fontWeight = FontWeight.Black)
            }
        }
    }
}
