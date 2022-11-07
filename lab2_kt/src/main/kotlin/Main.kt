import kotlin.math.roundToInt
import kotlin.math.sqrt
import kotlin.random.Random

fun main(args: Array<String>) {
    val original = "Codetest"
    val a = 12
    val u = 1234
    val m = 2972
    val Y0 = 3421
    val encoded = encode(original, a, u, m, Y0)
    println("Encoded: " + encoded.joinToString(""))
    val decoded = decode(encoded.joinToString(""), a, u, m, Y0)
    println("Decoded: " + decoded.joinToString(""))
}

fun getGamma(length: Int, a: Int, u: Int, m: Int, Y0: Int): List<Int> {
    val result = mutableListOf<Int>()
    result.add(Y0)
    for (i in 0 until length) {
        result.add((a*result[i] + u) % m)
    }
    return result;
}

fun encode(original: String, a: Int, u: Int, m: Int, Y0: Int): List<String> {
    val result = mutableListOf<String>()
    val chunkedOriginal = original.toList().map { it.toString() }.chunked(8)
    var gammaBuffer = listOf(Y0)
    for (elements in chunkedOriginal) {
        val firstY = gammaBuffer[gammaBuffer.size - 1]
        gammaBuffer = getGamma(elements.size, a, u, m, firstY)
        elements.forEachIndexed { index, s ->
            val code = s.first().code
            result.add(Char(code.xor(gammaBuffer[index])).toString())
        }
    }
    return result
}

fun decode(original: String, a: Int, u: Int, m: Int, Y0: Int): List<String> {
    return encode(original, a, u, m, Y0)
}