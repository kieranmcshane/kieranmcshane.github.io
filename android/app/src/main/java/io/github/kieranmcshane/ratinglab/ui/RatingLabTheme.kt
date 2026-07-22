package io.github.kieranmcshane.ratinglab.ui

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

val Ink = Color(0xFF172033)
val Muted = Color(0xFF667085)
val Canvas = Color(0xFFF3F1EB)
val Paper = Color(0xFFFCFBF8)
val Rule = Color(0xFFE1DED5)
val Cobalt = Color(0xFF3157C8)
val Positive = Color(0xFF18765B)
val Negative = Color(0xFFA44843)
val Violet = Color(0xFF6750A4)

private val RatingLabColors = lightColorScheme(
    primary = Cobalt,
    onPrimary = Color.White,
    secondary = Violet,
    onSecondary = Color.White,
    background = Canvas,
    onBackground = Ink,
    surface = Paper,
    onSurface = Ink,
    surfaceVariant = Color(0xFFEDEBE5),
    onSurfaceVariant = Muted,
    outline = Rule,
    error = Negative
)

@Composable
fun RatingLabTheme(content: @Composable () -> Unit) {
    MaterialTheme(colorScheme = RatingLabColors, content = content)
}
