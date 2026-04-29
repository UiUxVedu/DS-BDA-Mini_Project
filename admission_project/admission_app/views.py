from django.shortcuts import render, redirect
from .models import Admission
from .forms import AdmissionForm
from .ml_model import train_models
import pandas as pd
import os
from django.conf import settings
from .models import ModelHistory
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse

def home(request):
    import pandas as pd
    import os
    from django.conf import settings

    file_path = os.path.join(settings.BASE_DIR, "admission_app", "data", "admission_data.csv")
    df = pd.read_csv(file_path)

    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(" ", "_")

    preview = df.head(20).to_dict(orient='records')

    return render(request, "home.html", {
        "data": preview,
        "avg_cgpa": round(df["CGPA"].mean(), 2),
        "avg_gre": round(df["GRE_Score"].mean(), 2)
    })

def add_data(request):
    form = AdmissionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'add.html', {'form': form})

def predict(request):
    if request.method == "POST":

        gre = float(request.POST['gre'])
        toefl = float(request.POST['toefl'])
        cgpa = float(request.POST['cgpa'])
        sop = float(request.POST['sop'])
        lor = float(request.POST['lor'])
        research = int(request.POST['research'])

        selected_model = request.POST.get("model")

        # 🔥 TRAIN MODELS
        if selected_model == "best":
            results = train_models()
            best_model_name = max(results, key=lambda x: results[x]["r2"])
            model = results[best_model_name]["model"]

        else:
            results = train_models(selected_model)
            best_model_name = selected_model
            model = results[selected_model]["model"]

        # 🔥 SAVE HISTORY (IMPORTANT PART)
        for name, val in results.items():
            ModelHistory.objects.create(
                model_name=name,
                r2=val["r2"],
                mse=val["mse"],
                mae=val["mae"]
            )

        # 🔥 PREDICTION
        prediction = model.predict([[gre, toefl, cgpa, sop, lor, research]])

        return render(request, "result.html", {
            "result": prediction[0],
            "best_model": best_model_name,
            "all_results": results
        })

    return render(request, "predict.html")


def analytics(request):
    results = train_models()
    return render(request, "analytics.html", {"results": results})

def history(request):
    data = ModelHistory.objects.all().order_by('-created_at')
    return render(request, "history.html", {"history": data})

def export_pdf(request):
    result = request.GET.get("result")
    model = request.GET.get("model")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("Admission Prediction Report", styles['Title']))
    content.append(Spacer(1, 20))

    content.append(Paragraph(f"Prediction: {result}", styles['Normal']))
    content.append(Paragraph(f"Model Used: {model}", styles['Normal']))

    doc.build(content)

    return response


def export_pdf(request):
    result = request.GET.get("result")
    model = request.GET.get("model")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("Admission Prediction Report", styles['Title']))
    content.append(Spacer(1, 20))

    content.append(Paragraph(f"Prediction: {result}", styles['Normal']))
    content.append(Paragraph(f"Model Used: {model}", styles['Normal']))

    doc.build(content)

    return response