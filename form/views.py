from django.shortcuts import redirect, render
from .models import Form, Questions, Response, ResponseQuestion
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages


def main_dashbord(request):
    return render(request , 'form/index.html')


############ show forms created by user, to see or delete them #################
@login_required(login_url='/auth/login/')
def my_form(request):
    try:
        forms = Form.objects.filter(user__id = request.user.id)[::-1]
    except:
        forms= None
    return render(request , 'form/my_form.html' , {'forms': forms})


#################################### creating form and questions ###################################
@login_required(login_url='/auth/login/')
def create_form(request):
    if request.method == "POST":
        Form(name=request.POST["form-name"] , user_id= request.user.id).save()
        f = Form.objects.filter(name=request.POST["form-name"])[::-1][0]

        for i in range(int(request.POST["questionCount"])):
            try:
                Questions(label=request.POST[str(i)], form=f).save()
            except:
                pass
        return HttpResponseRedirect(reverse('form:myform'))
    return render(request, "form/create.html")


############################### delete form and its Q&A ##########################################
def delete_form(request, form):
    Form.objects.filter(id=form).delete()
    return redirect(reverse('form:myform'))


######### placing questions in form and make form ready to share with participants ##########
def view_form(request, form):
    try:
        f = Form.objects.get(id=form)
    except:
        return HttpResponse("404 Not Found")
    frm = Form.objects.filter(id = form)
    questions = Questions.objects.filter(form__id=f.id)
    formname = frm[0].name
    return render(request, "form/view-form.html", {
        "form": form,
        "questions": questions,
        "name":formname
    })


########## receiving participants answer and create submission ##############################
def submit_form(request, form):
    ############## creating response form ###########
    questions = Questions.objects.filter(form__id = form)
    response = Response(question= questions[0])
    response.save()
    ############## preparing response form ##########
    resp = Response.objects.filter(question= questions[0])[::-1][0]

    ######## connecting questions and answers, and put them in response form #######
    for i in request.POST:
        if i == "csrfmiddlewaretoken":
            continue
        ResponseQuestion(question_id=i, response=request.POST[i], response_id=resp.id).save()

    messages.success(request, "Your answers has been submited:)")
    return redirect(reverse("form:index"))
#    return HttpResponseRedirect(f"/d/{form_id}/{r.id}/")


#############################################################################################


############# user can see form link, questions, and participants answers ################## 
def form_details(request , form):
    frm = Form.objects.get(user_id = request.user.id , id = form)
    question = Questions.objects.filter(form__id = form)[0]
    response = Response.objects.filter(question = question)
    questions = Questions.objects.filter(form__id = form)
    participants = len(question.response_set.all())
    return render(request , "form/form.html" , {'questions': questions,'form': frm ,
     'participants':participants , 'response':response})


################ see participants answers #############################################
def view_all_submission(request, form , submission):
    try:
        form = Form.objects.get(id=form)
        questions = Questions.objects.filter(form__id = form.id)
        ########################################################
        rs = Response.objects.filter(question= questions[0])[::-1]
        rs2 = []
        i = 1
        for r in rs:
            rs2.append([r , i])
            i+=1

        ##############################################################
        rss = ResponseQuestion.objects.filter(response_id = submission)
        data = []
        for r in rss:
            i = Questions.objects.get(id = r.question_id)
            data.append([i.label , r.response])

    except:
        messages.warning(request, "there is no response yet")
        return HttpResponseRedirect(reverse('form:myform'))
    return render(request , 'form/view-response.html' , {'data':data , 'rs':rs2[::-1] , 'form':form})
