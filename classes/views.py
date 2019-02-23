from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Classroom , Student
from .forms import ClassroomForm ,StudentForm , SingUpForm , SingInForm 
from django.contrib.auth import authenticate, login, logout

 


def signup(request):
	form = SingUpForm()
	if request.method == "POST":
		form = SingUpForm(request.POST)
		if form.is_valid():
			user_obj = form.save(commit=False)
			user_obj.set_password(user_obj.password)
			user_obj.save()
			login(request, user_obj)
			return redirect('classroom-list')
	context = {
	  "form": form,
	}
	return render(request, 'signup.html', context)

def signin(request):
	form = SingInForm()
	if request.method == "POST":
		form = SingInForm(request.POST)
		if form.is_valid():
			my_username = form.cleaned_data['username']
			my_password = form.cleaned_data['password']
			user_obj= authenticate (username=my_username, password=my_password)
			if user_obj is not None:
				login(request, user_obj)
			return redirect('classroom-list')
	context = {
	  "form": form,
	}
	return render(request, 'signin.html', context)

def signout(request):
	logout(request)
	return redirect('signin')

def classroom_list(request):
	classrooms = Classroom.objects.all()
	context = {
		"classrooms": classrooms,
	}
	return render(request, 'classroom_list.html', context)


def classroom_detail(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
 	 
	context = {
		"classroom": classroom,
 	}
	return render(request, 'classroom_detail.html', context)


def classroom_create(request):
	form = ClassroomForm()
	if request.method == "POST":
		form = ClassroomForm(request.POST, request.FILES or None)
		if form.is_valid():
			classroom= form.save(commit=False)
			classroom.teacher = request.user
			form.save()
			messages.success(request, "Successfully Created!")
			return redirect('classroom-list')
		print (form.errors)
	context = {
	"form": form,
	}
	return render(request, 'create_classroom.html', context)

def student_add(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	if not (request.user == classroom.teacher):
		messages.success(request, 'You can not bro')
		return redirect('classroom-list')

	form = StudentForm()
	if request.method == "POST":
		form = StudentForm(request.POST)
		if form.is_valid():
			student= form.save(commit=False)
			student.classroom = classroom
			form.save()
			messages.success(request, 'well done !')
			return redirect('classroom-detail' ,classroom_id=classroom_id)
		print(form.errors)
	context = {
	"form": form,
	"classroom": classroom,
	}
	return render(request, 'student_add.html', context)


def student_update(request, student_id, classroom_id):
	student = Student.objects.get(id=student_id)
	if not (request.user == student.classroom.teacher):
		messages.success(request, 'nooop you can not !')
		return redirect('classroom-list')

	form = StudentForm(instance=student)
	if request.method == "POST":
		form = StudentForm(request.POST, instance=student)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Edited!")
			return redirect('classroom-detail', classroom_id=classroom_id)
		print (form.errors)
	context = {
	"form": form,
	"student":student,
	"classroom_id": classroom_id

	}
	return render(request, 'update_student.html', context)


def classroom_update(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	if not (request.user == classroom.teacher):
		messages.success(request, 'nooop you can not !')
		return redirect('classroom-list')
	form = ClassroomForm(instance=classroom)
	if request.method == "POST":
		form = ClassroomForm(request.POST, request.FILES or None, instance=classroom)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Edited!")
			return redirect('classroom-list')
		print (form.errors)
	context = {
	"form": form,
	"classroom": classroom,
	}
	return render(request, 'update_classroom.html', context)


def classroom_delete(request, classroom_id):
	 classroom = Classroom.objects.get(id=classroom_id)
	 if not (request.user == classroom.teacher):
	 	messages.success(request, "sd!")
	 	return redirect('classroom-list')
	 classroom.delete()
	 messages.success(request, "Successfully Deleted!")
	 return redirect('classroom-list')
	
def student_delete(request, student_id, classroom_id):
	 student = Student.objects.get(id=student_id)
	 if not (request.user == student.classroom.teacher):
	 	messages.success(request, "sd!")
	 	return redirect('classroom-list')
	 classroom_id=student.classroom_id	
	 student.delete()
	 messages.success(request, "Successfully Deleted!")
	 return redirect('classroom-detail', classroom_id=classroom_id)
