import { Routes } from '@angular/router';
import { StudentDetailsComponent } from './student-details/student-details.component';
import { ClassRegistrationComponent } from './class-registration/class-registration.component';
import { ScheduleCourseComponent } from './schedule-course/schedule-course.component';
import {RegistrationComponent} from './registration/registration.component';
import {LoginComponent} from './login/login.component';
import {ApplicantDetailsComponent} from './applicant-details/applicant-details.component';
import {ProfileComponent} from './profile/profile.component';

export const routes: Routes = [
    {path: '', redirectTo: '/login', pathMatch: 'full' },
    {path: 'login', component: LoginComponent},
    {path: 'registration', component: RegistrationComponent},
    {path: 'applicant-details', component: ApplicantDetailsComponent},
    {path: 'student-details', component: StudentDetailsComponent},
    {path: 'class-registration', component: ClassRegistrationComponent},
    {path: 'schedule-course', component: ScheduleCourseComponent},
    {path: 'profile', component: ProfileComponent}
];
