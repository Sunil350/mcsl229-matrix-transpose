from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Matrix Transpose - Google App Engine</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f9f9fb; color: #222; }
        .container { max-width: 600px; background: #fff; padding: 24px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
        textarea { width: 100%; height: 110px; font-family: monospace; font-size: 14px; padding: 8px; box-sizing: border-box; }
        button { background: #1a73e8; color: #fff; border: none; padding: 10px 18px; border-radius: 4px; cursor: pointer; font-size: 14px; }
        button:hover { background: #1557b0; }
        table { border-collapse: collapse; margin-top: 10px; margin-bottom: 20px; }
        td { border: 1px solid #444; padding: 8px 16px; text-align: center; background: #f4f6f8; }
        .error { color: #c5221f; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Matrix Transpose on Google App Engine</h2>
        <p><strong>Course:</strong> MCSL-229 (Cloud & Data Science Lab)</p>
        <form method="POST">
            <label for="matrix">Enter matrix rows (comma-separated values, one row per line):</label><br><br>
            <textarea id="matrix" name="matrix">{{ matrix_input }}</textarea><br><br>
            <button type="submit">Find Transpose</button>
        </form>

        {% if error %}
            <p class="error">{{ error }}</p>
        {% endif %}

        {% if original and not error %}
            <h3>Original Matrix ({{ original|length }} x {{ original[0]|length }}):</h3>
            <table>
                {% for row in original %}
                    <tr>{% for val in row %}<td>{{ val }}</td>{% endfor %}</tr>
                {% endfor %}
            </table>

            <h3>Transposed Matrix ({{ transposed|length }} x {{ transposed[0]|length }}):</h3>
            <table>
                {% for row in transposed %}
                    <tr>{% for val in row %}<td>{{ val }}</td>{% endfor %}</tr>
                {% endfor %}
            </table>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def transpose_matrix():
    default_input = "1, 2, 3\n4, 5, 6"
    matrix_input = request.form.get("matrix", default_input)
    original = []
    transposed = []
    error = None

    rows = [r.strip() for r in matrix_input.strip().split("\n") if r.strip()]
    if rows:
        original = [[item.strip() for item in row.split(",")] for row in rows]
        row_lengths = {len(r) for r in original}
        if len(row_lengths) > 1:
            error = "All rows must have the same number of columns."
        else:
            transposed = [list(col) for col in zip(*original)]

    return render_template_string(
        HTML_TEMPLATE,
        matrix_input=matrix_input,
        original=original,
        transposed=transposed,
        error=error
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
