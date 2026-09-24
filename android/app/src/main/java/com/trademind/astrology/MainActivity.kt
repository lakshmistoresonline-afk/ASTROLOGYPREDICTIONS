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
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Star
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
                    val selectedPlanet = viewModel.selectedPlanetForInspection
                    
                    if (selectedPlanet != null) {
                        PlanetaryInspectorSheet(selectedPlanet) { viewModel.selectedPlanetForInspection = null }
                    }

                    when (currentScreen) {
                        is Screen.Login -> LoginScreen(viewModel)
                        is Screen.BirthProfile -> BirthProfileScreen(viewModel)
                        is Screen.Dashboard -> DashboardScreen(viewModel)
                        is Screen.PredictionDetail -> PredictionDetailScreen(viewModel, currentScreen.domain)
                        is Screen.ChartVisualizer -> ChartVisualizerScreen(viewModel)
                        is Screen.CompatibilityHub -> CompatibilityHubScreen(viewModel)
                        is Screen.TimingHub -> AuspiciousTimingScreen(viewModel)
                    }
                }
            }
        }
    }
}

sealed class Screen {
    object Login : Screen()
    object BirthProfile : Screen()
    object Dashboard : Screen()
    data class PredictionDetail(val domain: String) : Screen()
    object ChartVisualizer : Screen()
    object CompatibilityHub : Screen()
    object TimingHub : Screen()
}

@Composable
fun LoginScreen(viewModel: MainViewModel) {
    Column(
        modifier = Modifier.fillMaxSize().padding(32.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Icon(
            imageVector = androidx.compose.material.icons.Icons.Default.Star,
            contentDescription = null,
            tint = Color(0xFFFBBF24),
            modifier = Modifier.size(64.dp)
        )
        Spacer(modifier = Modifier.height(16.dp))
        Text("Jyotish Intelligence", fontSize = 24.sp, fontWeight = FontWeight.Black, color = Color.White)
        Text("PROFESSIONAL PREDICTION OS", fontSize = 12.sp, color = Color(0xFFFBBF24), letterSpacing = 2.sp)
        
        Spacer(modifier = Modifier.height(48.dp))
        
        Button(
            onClick = { viewModel.currentScreen = Screen.BirthProfile },
            modifier = Modifier.fillMaxWidth().height(56.dp),
            shape = RoundedCornerShape(12.dp),
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFFBBF24))
        ) {
            Text("ENTER AS TESTER", color = Color.Black, fontWeight = FontWeight.Black)
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        OutlinedButton(
            onClick = { viewModel.currentScreen = Screen.BirthProfile },
            modifier = Modifier.fillMaxWidth().height(56.dp),
            shape = RoundedCornerShape(12.dp),
            border = androidx.compose.foundation.BorderStroke(1.dp, Color.Gray)
        ) {
            Text("ADMINISTRATIVE BYPASS", color = Color.White)
        }
        
        Spacer(modifier = Modifier.height(32.dp))
        Text(
            "Version 3.22.5 • Developer Preview\nStandard Firebase protocols are mocked.",
            fontSize = 10.sp,
            color = Color.Gray,
            textAlign = androidx.compose.ui.text.style.TextAlign.Center
        )
    }
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
            Row(modifier = Modifier.fillMaxWidth().padding(top = 8.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Button(
                    onClick = { viewModel.currentScreen = Screen.ChartVisualizer },
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF1E293B)),
                    modifier = Modifier.weight(1f)
                ) {
                    Text("VIEW CHARTS", color = Color(0xFFFBBF24), fontWeight = FontWeight.Bold, fontSize = 11.sp)
                }
                Button(
                    onClick = { viewModel.currentScreen = Screen.CompatibilityHub },
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF1E293B)),
                    modifier = Modifier.weight(1f)
                ) {
                    Text("MATCHMAKING", color = Color(0xFFFBBF24), fontWeight = FontWeight.Bold, fontSize = 11.sp)
                }
                Button(
                    onClick = { viewModel.currentScreen = Screen.TimingHub },
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF1E293B)),
                    modifier = Modifier.weight(1f)
                ) {
                    Text("TIMING", color = Color(0xFFFBBF24), fontWeight = FontWeight.Bold, fontSize = 11.sp)
                }
            }
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
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column {
            Text("Namaste", fontSize = 24.sp, fontWeight = FontWeight.Black, color = Color.White)
            Text("ASTRO PREDICTIONS V3.36", fontSize = 12.sp, color = Color(0xFFFBBF24), letterSpacing = 2.sp)
        }
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

@Composable
fun ChartVisualizerScreen(viewModel: MainViewModel) {
    val data = viewModel.dashboardData
    var selectedVarga by remember { mutableStateOf("D1") }

    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            IconButton(onClick = { viewModel.currentScreen = Screen.Dashboard }) {
                Text("<", color = Color.White, fontSize = 24.sp)
            }
            Text("Visual Intelligence Canvas", fontSize = 18.sp, fontWeight = FontWeight.Black, color = Color.White)
        }

        Spacer(modifier = Modifier.height(12.dp))

        // Varga Selection Tabs
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            listOf("D1", "D9", "D10").forEach { varga ->
                FilterChip(
                    selected = selectedVarga == varga,
                    onClick = { selectedVarga = varga },
                    label = { Text(varga, color = Color.White) }
                )
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        Box(
            modifier = Modifier
                .fillMaxWidth()
                .aspectRatio(1f)
                .background(Color(0xFF1E293B), shape = RoundedCornerShape(16.dp))
                .padding(16.dp),
            contentAlignment = Alignment.Center
        ) {
            // High Fidelity Vector Chart Canvas (North Indian Style Layout)
            androidx.compose.foundation.Canvas(modifier = Modifier.fillMaxSize()) {
                val size = this.size.width
                
                // Draw Outer bounding border box
                drawRect(
                    color = Color(0xFFFBBF24),
                    style = androidx.compose.ui.graphics.drawscope.Stroke(width = 3.dp.toPx())
                )

                // Diagonal Line crossings
                drawLine(color = Color(0xFFFBBF24), start = androidx.compose.ui.geometry.Offset(0f, 0f), end = androidx.compose.ui.geometry.Offset(size, size), strokeWidth = 2.dp.toPx())
                drawLine(color = Color(0xFFFBBF24), start = androidx.compose.ui.geometry.Offset(size, 0f), end = androidx.compose.ui.geometry.Offset(0f, size), strokeWidth = 2.dp.toPx())

                // Inner diamond matrix connection loops
                drawLine(color = Color(0xFFFBBF24), start = androidx.compose.ui.geometry.Offset(size / 2f, 0f), end = androidx.compose.ui.geometry.Offset(0f, size / 2f), strokeWidth = 1.5.dp.toPx())
                drawLine(color = Color(0xFFFBBF24), start = androidx.compose.ui.geometry.Offset(0f, size / 2f), end = androidx.compose.ui.geometry.Offset(size / 2f, size), strokeWidth = 1.5.dp.toPx())
                drawLine(color = Color(0xFFFBBF24), start = androidx.compose.ui.geometry.Offset(size / 2f, size), end = androidx.compose.ui.geometry.Offset(size, size / 2f), strokeWidth = 1.5.dp.toPx())
                drawLine(color = Color(0xFFFBBF24), start = androidx.compose.ui.geometry.Offset(size, size / 2f), end = androidx.compose.ui.geometry.Offset(size / 2f, 0f), strokeWidth = 1.5.dp.toPx())
            }

            // Overlay indicator badge context
            Text(
                text = "Varga Matrix: $selectedVarga",
                color = Color(0xFFFBBF24),
                fontWeight = FontWeight.Black,
                fontSize = 14.sp
            )
        }

        Spacer(modifier = Modifier.height(24.dp))

        Text("PLANETARY ALIGNMENTS & DIGNITIES", fontSize = 12.sp, fontWeight = FontWeight.Black, color = Color.Gray)
        
        Spacer(modifier = Modifier.height(8.dp))

        LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            val planets = data?.planets ?: emptyList()
            if (planets.isEmpty()) {
                item { Text("No planetary alignment snapshot loaded.", color = Color.White, fontSize = 12.sp) }
            } else {
                items(planets) { p ->
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .background(Color(0xFF1E293B), RoundedCornerShape(12.dp))
                            .clickable { viewModel.selectedPlanetForInspection = p }
                            .padding(12.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column {
                            Row {
                                Text(p.name, fontWeight = FontWeight.Bold, color = Color.White)
                                if (p.is_retrograde) {
                                    Text(" (R)", color = Color(0xFFF59E0B), fontWeight = FontWeight.Bold)
                                }
                                if (p.is_combust) {
                                    Text(" (C)", color = Color.Red, fontWeight = FontWeight.Bold)
                                }
                            }
                            Text("House ${p.house} • Rashi ${p.rashi + 1}", fontSize = 12.sp, color = Color.Gray)
                        }

                        val textColor = when (p.dignity) {
                            "Exalted" -> Color(0xFFFBBF24)
                            "Debilitated" -> Color.Red
                            "Own Sign" -> Color(0xFF4ADE80)
                            else -> Color.White
                        }
                        Text(p.dignity.uppercase(), fontWeight = FontWeight.Black, fontSize = 11.sp, color = textColor)
                    }
                }

                item {
                    Spacer(modifier = Modifier.height(24.dp))
                    AshtakavargaMatrixWidget(data)
                }
                
                item {
                    Spacer(modifier = Modifier.height(24.dp))
                    BhavaBalaHeatmap(data)
                }

                item {
                    Spacer(modifier = Modifier.height(24.dp))
                    Text("PRATYANTAR MICRO-TIMING (WEEKS)", fontSize = 12.sp, fontWeight = FontWeight.Black, color = Color.Gray)
                    Spacer(modifier = Modifier.height(8.dp))
                    val pratyantars = data?.pratyantar_dasha ?: emptyList()
                    if (pratyantars.isEmpty()) {
                        Text("No micro-timing data for current window.", color = Color.Gray, fontSize = 12.sp)
                    } else {
                        pratyantars.forEach { p ->
                            Card(
                                colors = CardDefaults.cardColors(containerColor = Color(0xFF1E293B).copy(alpha = 0.5f)),
                                modifier = Modifier.fillMaxWidth().padding(bottom = 4.dp)
                            ) {
                                Row(modifier = Modifier.padding(12.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                    Text(p.lord, color = Color.White, fontWeight = FontWeight.Bold)
                                    Text("${p.start} - ${p.end}", color = Color.Gray, fontSize = 10.sp)
                                }
                            }
                        }
                    }
                }

                item {
                    Spacer(modifier = Modifier.height(24.dp))
                    Text("Jaimini Chara Dasha Sequence", fontSize = 12.sp, fontWeight = FontWeight.Black, color = Color.Gray)
                    Spacer(modifier = Modifier.height(8.dp))
                    val dashas = data?.chara_dasha ?: emptyList()
                    if (dashas.isNotEmpty()) {
                        dashas.forEach { stream ->
                            Card(colors = CardDefaults.cardColors(containerColor = Color(0xFF1E293B).copy(alpha = 0.6f)), modifier = Modifier.fillMaxWidth().padding(bottom = 6.dp)) {
                                Text(stream, modifier = Modifier.padding(12.dp), color = Color(0xFFFBBF24), fontWeight = FontWeight.Bold, fontSize = 13.sp)
                            }
                        }
                    }
                }

                item {
                    Spacer(modifier = Modifier.height(24.dp))
                    Text("CROSS-SYSTEM CONVERSANT SYNTHESIS HUB", fontSize = 12.sp, fontWeight = FontWeight.Black, color = Color.Gray)
                    Spacer(modifier = Modifier.height(8.dp))
                    Card(colors = CardDefaults.cardColors(containerColor = Color(0xFF1E293B)), modifier = Modifier.fillMaxWidth()) {
                        Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                            Text("🇨🇳 CHINESE BAZI FOUR PILLARS", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 12.sp)
                            data?.bazi_pillars?.forEach { pillar ->
                                Text("• $pillar", color = Color.LightGray, fontSize = 13.sp)
                            }
                            Spacer(modifier = Modifier.height(4.dp))
                            Text("🏛️ HELLENISTIC RELEASING TIMELORDS", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 12.sp)
                            Text(data?.hellenistic_releasing ?: "Level 1 Scanning Active...", color = Color.LightGray, fontSize = 13.sp)
                            Spacer(modifier = Modifier.height(4.dp))
                            Text("🧬 HUMAN DESIGN GENE KEYS PROFILE", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 12.sp)
                            Text(data?.gene_keys_profile ?: "Core Synthesis Active...", color = Color.LightGray, fontSize = 13.sp)
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun CompatibilityHubScreen(viewModel: MainViewModel) {
    var boyName by remember { mutableStateOf("") }
    var boyDob by remember { mutableStateOf("") }
    var boyPlace by remember { mutableStateOf("") }

    var girlName by remember { mutableStateOf("") }
    var girlDob by remember { mutableStateOf("") }
    var girlPlace by remember { mutableStateOf("") }

    val res = viewModel.compatibilityData
    val compError = viewModel.compatibilityError
    val isCompLoading = viewModel.isCompatibilityLoading

    LazyColumn(modifier = Modifier.fillMaxSize().padding(16.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
        item {
            Row(verticalAlignment = Alignment.CenterVertically) {
                IconButton(onClick = { viewModel.currentScreen = Screen.Dashboard }) {
                    Text("<", color = Color.White, fontSize = 24.sp)
                }
                Text("Ashtakoota Matchmaking Hub", fontSize = 18.sp, fontWeight = FontWeight.Black, color = Color.White)
            }
        }

        item {
            Card(colors = CardDefaults.cardColors(containerColor = Color(0xFF1E293B)), shape = RoundedCornerShape(16.dp)) {
                Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                    Text("Boy's Profile", color = Color(0xFFFBBF24), fontWeight = FontWeight.Bold)
                    OutlinedTextField(value = boyName, onValueChange = { boyName = it }, label = { Text("Name") }, modifier = Modifier.fillMaxWidth())
                    OutlinedTextField(value = boyDob, onValueChange = { boyDob = it }, label = { Text("Date (YYYY-MM-DD)") }, modifier = Modifier.fillMaxWidth())
                    OutlinedTextField(value = boyPlace, onValueChange = { boyPlace = it }, label = { Text("Birth Place") }, modifier = Modifier.fillMaxWidth())

                    Divider(color = Color.Gray.copy(alpha = 0.3f), modifier = Modifier.padding(vertical = 4.dp))

                    Text("Girl's Profile", color = Color(0xFFFBBF24), fontWeight = FontWeight.Bold)
                    OutlinedTextField(value = girlName, onValueChange = { girlName = it }, label = { Text("Name") }, modifier = Modifier.fillMaxWidth())
                    OutlinedTextField(value = girlDob, onValueChange = { girlDob = it }, label = { Text("Date (YYYY-MM-DD)") }, modifier = Modifier.fillMaxWidth())
                    OutlinedTextField(value = girlPlace, onValueChange = { girlPlace = it }, label = { Text("Birth Place") }, modifier = Modifier.fillMaxWidth())

                    Spacer(modifier = Modifier.height(8.dp))

                    Button(
                        onClick = { viewModel.calculateCompatibility(boyName, boyDob, boyPlace, girlName, girlDob, girlPlace) },
                        modifier = Modifier.fillMaxWidth(),
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFFBBF24)),
                        enabled = boyDob.isNotBlank() && boyPlace.isNotBlank() && girlDob.isNotBlank() && girlPlace.isNotBlank()
                    ) {
                        Text("COMPUTE KUTA COMPATIBILITY", color = Color.Black, fontWeight = FontWeight.Black)
                    }
                }
            }
        }

        if (isCompLoading) {
            item {
                Box(modifier = Modifier.fillMaxWidth(), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator(color = Color(0xFFFBBF24))
                }
            }
        }

        if (compError != null) {
            item {
                Text(compError ?: "", color = Color.Red, fontSize = 12.sp, fontWeight = FontWeight.Bold)
            }
        }

        if (res != null) {
            item {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(
                            brush = Brush.horizontalGradient(listOf(Color(0xFFFBBF24), Color(0xFFF59E0B))),
                            shape = RoundedCornerShape(16.dp)
                        )
                        .padding(24.dp)
                ) {
                    Column {
                        Text("COMPATIBILITY ANALYSIS BALANCE", fontSize = 10.sp, fontWeight = FontWeight.Black, color = Color.Black.copy(alpha = 0.6f))
                        Text("${res.total_score} / ${res.max_score} Gunas", fontSize = 28.sp, fontWeight = FontWeight.Black, color = Color.Black)
                        Text("Verdict: ${res.verdict}", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.Black)
                    }
                }
            }

            item {
                Text("DETAILED KUTA REPORT MATRIX", fontSize = 12.sp, fontWeight = FontWeight.Black, color = Color.Gray)
            }

            items(res.kutas) { k ->
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(Color(0xFF1E293B), RoundedCornerShape(12.dp))
                        .padding(16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column {
                        Text(k.name, fontWeight = FontWeight.Bold, color = Color.White)
                        Text("Score: ${k.score} of ${k.max}", fontSize = 12.sp, color = Color.Gray)
                    }
                    val badgeColor = if (k.status == "PASS") Color(0xFF4ADE80) else Color.Red
                    Text(k.status, color = badgeColor, fontWeight = FontWeight.Black, fontSize = 11.sp)
            }
        }
    }
}

@Composable
fun AshtakavargaMatrixWidget(data: DashboardResponse?) {
    val avMap = data?.ashtakavarga ?: emptyMap()
    val sarva = avMap["Sarva"] as? Map<*, *> ?: emptyMap()

    Column(modifier = Modifier.fillMaxWidth()) {
        Text("ASHTAKAVARGA BINDU DISTRIBUTION", fontSize = 12.sp, fontWeight = FontWeight.Black, color = Color.Gray)
        Spacer(modifier = Modifier.height(12.dp))

        Card(
            colors = CardDefaults.cardColors(containerColor = Color(0xFF1E293B)),
            shape = RoundedCornerShape(16.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("SARVASTAKAVARGA (TOTAL VITALITY)", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 12.sp)
                Spacer(modifier = Modifier.height(12.dp))

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(4.dp)
                ) {
                    (0..11).forEach { rashiIdx ->
                        val bindusValue = sarva[rashiIdx.toString()]
                        val bindus = when (bindusValue) {
                            is Double -> bindusValue.toInt()
                            is String -> bindusValue.toIntOrNull() ?: 0
                            else -> 0
                        }
                        
                        val bgColor = when {
                            bindus >= 30 -> Color(0xFF4ADE80).copy(alpha = 0.2f)
                            bindus < 20 -> Color.Red.copy(alpha = 0.2f)
                            else -> Color.Transparent
                        }
                        val borderColor = when {
                            bindus >= 30 -> Color(0xFF4ADE80)
                            bindus < 20 -> Color.Red
                            else -> Color.Gray.copy(alpha = 0.5f)
                        }

                        Box(
                            modifier = Modifier
                                .weight(1f)
                                .aspectRatio(0.8f)
                                .background(bgColor, RoundedCornerShape(4.dp))
                                .border(1.dp, borderColor, RoundedCornerShape(4.dp)),
                            contentAlignment = Alignment.Center
                        ) {
                            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                Text("${rashiIdx + 1}", fontSize = 8.sp, color = Color.Gray)
                                Text("$bindus", fontSize = 11.sp, fontWeight = FontWeight.Black, color = Color.White)
                            }
                        }
                    }
                }
                
                Spacer(modifier = Modifier.height(12.dp))
                Text("Houses with >30 bindus indicate high-yield life areas, while <20 indicates structural friction.", fontSize = 10.sp, color = Color.Gray)
            }
        }
    }
}

@Composable
fun BhavaBalaHeatmap(data: DashboardResponse?) {
    val bbMap = data?.bhava_bala ?: emptyMap()
    
    Column(modifier = Modifier.fillMaxWidth()) {
        Text("HOUSE VITALITY HEATMAP (BHAVA BALA)", fontSize = 12.sp, fontWeight = FontWeight.Black, color = Color.Gray)
        Spacer(modifier = Modifier.height(12.dp))
        
        Card(
            colors = CardDefaults.cardColors(containerColor = Color(0xFF1E293B)),
            shape = RoundedCornerShape(16.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                    (1..12).forEach { house ->
                        val score = bbMap[house.toString()] ?: 0.0
                        // Heatmap color: 0-50 scale. >35 is strong.
                        val alpha = (score / 50.0).coerceIn(0.1, 1.0).toFloat()
                        val color = if (score > 35) Color(0xFF4ADE80) else Color(0xFFFBBF24)
                        
                        Box(
                            modifier = Modifier
                                .weight(1f)
                                .aspectRatio(0.6f)
                                .background(color.copy(alpha = alpha * 0.3f), RoundedCornerShape(4.dp))
                                .border(1.dp, color.copy(alpha = alpha), RoundedCornerShape(4.dp)),
                            contentAlignment = Alignment.Center
                        ) {
                            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                Text("H$house", fontSize = 8.sp, color = Color.Gray)
                                Text("${score.toInt()}", fontSize = 10.sp, fontWeight = FontWeight.Bold, color = Color.White)
                            }
                        }
                    }
                }
                Spacer(modifier = Modifier.height(8.dp))
                Text("Higher intensity signals peak structural support for that life area.", fontSize = 9.sp, color = Color.Gray)
            }
        }
    }
}

@Composable
fun AuspiciousTimingScreen(viewModel: MainViewModel) {
    LaunchedEffect(Unit) {
        viewModel.fetchMuhurta()
    }
    
    val data = viewModel.muhurtaData
    
    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            IconButton(onClick = { viewModel.currentScreen = Screen.Dashboard }) {
                Text("<", color = Color.White, fontSize = 24.sp)
            }
            Text("Daily Auspicious Timing Hub", fontSize = 18.sp, fontWeight = FontWeight.Black, color = Color.White)
        }

        if (viewModel.isMuhurtaLoading) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                CircularProgressIndicator(color = Color(0xFFFBBF24))
            }
        } else if (data != null) {
            LazyColumn(verticalArrangement = Arrangement.spacedBy(16.dp), modifier = Modifier.padding(top = 16.dp)) {
                item {
                    SectionHeader("ELITE MUHURTA WINDOWS")
                    Row(modifier = Modifier.fillMaxWidth().padding(top = 8.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Card(modifier = Modifier.weight(1f), colors = CardDefaults.cardColors(containerColor = Color(0xFF1E293B))) {
                            Column(modifier = Modifier.padding(12.dp)) {
                                Text("ABHIJIT", fontSize = 10.sp, color = Color.Gray)
                                Text("${data.abhijit_muhurta.start} - ${data.abhijit_muhurta.end}", color = Color(0xFFFBBF24), fontWeight = FontWeight.Bold, fontSize = 11.sp)
                            }
                        }
                        Card(modifier = Modifier.weight(1f), colors = CardDefaults.cardColors(containerColor = Color(0xFF1E293B))) {
                            Column(modifier = Modifier.padding(12.dp)) {
                                Text("BRAHMA", fontSize = 10.sp, color = Color.Gray)
                                Text("${data.brahma_muhurta.start} - ${data.brahma_muhurta.end}", color = Color(0xFFFBBF24), fontWeight = FontWeight.Bold, fontSize = 11.sp)
                            }
                        }
                    }
                }

                item {
                    SectionHeader("CHOGHADIYA TIMELINE")
                }

                items(data.choghadiya) { period ->
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .background(Color(0xFF1E293B), RoundedCornerShape(12.dp))
                            .padding(16.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column {
                            Text(period.name, fontWeight = FontWeight.Black, color = if (period.is_auspicious) Color(0xFFFBBF24) else Color.White)
                            Text("${period.start} to ${period.end}", fontSize = 12.sp, color = Color.Gray)
                        }
                        if (period.is_auspicious) {
                            Text("AUSPICIOUS", color = Color(0xFF4ADE80), fontSize = 10.sp, fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PlanetaryInspectorSheet(planet: com.trademind.astrology.api.PlanetUiData, onDismiss: () -> Unit) {
    ModalBottomSheet(onDismissRequest = onDismiss, containerColor = Color(0xFF1E293B)) {
        Column(modifier = Modifier.fillMaxWidth().padding(24.dp).padding(bottom = 32.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
            Text("${planet.name.uppercase()} TECHNICAL DATASHEET", fontSize = 18.sp, fontWeight = FontWeight.Black, color = Color.White)
            
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Column {
                    Text("SHADBALA POTENCY", fontSize = 10.sp, color = Color.Gray)
                    Text("${planet.strength_rupas ?: 0.0} Rupas", fontSize = 24.sp, fontWeight = FontWeight.Black, color = Color(0xFFFBBF24))
                }
                if (planet.fixed_star_label != null) {
                    Column(horizontalAlignment = Alignment.End) {
                        Text("FIXED STAR CONJUNCTION", fontSize = 10.sp, color = Color.Gray)
                        Text(planet.fixed_star_label ?: "", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color(0xFF4ADE80))
                    }
                }
            }

            Divider(color = Color.Gray.copy(alpha = 0.2f))

            Text("STRUCTURAL STRENGTH FACTORS", fontSize = 11.sp, fontWeight = FontWeight.Black, color = Color.Gray)
            
            val factors = planet.strength_factors ?: emptyList()
            if (factors.isEmpty()) {
                Text("Standard functional vitality detected.", color = Color.LightGray, fontSize = 13.sp)
            } else {
                factors.forEach { f ->
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(modifier = Modifier.size(6.dp).background(Color(0xFFFBBF24), RoundedCornerShape(3.dp)))
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(f, color = Color.White, fontSize = 13.sp)
                    }
                }
            }

            Spacer(modifier = Modifier.height(16.dp))
            Button(
                onClick = onDismiss,
                modifier = Modifier.fillMaxWidth(),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF334155))
            ) {
                Text("CLOSE INSPECTOR", color = Color.White)
            }
        }
    }
}
