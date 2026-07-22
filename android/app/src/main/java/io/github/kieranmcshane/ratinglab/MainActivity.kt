package io.github.kieranmcshane.ratinglab

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import io.github.kieranmcshane.ratinglab.ui.RatingLabApp
import io.github.kieranmcshane.ratinglab.ui.RatingLabTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            RatingLabTheme {
                RatingLabApp()
            }
        }
    }
}
