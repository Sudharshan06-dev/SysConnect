import { Routes } from '@angular/router';
import { StudentDetailsComponent } from './student/student-details/student-details.component';
import { ClassRegistrationComponent } from './student/class-registration/class-registration.component';
import { ScheduleCourseComponent } from './admin/schedule-course/schedule-course.component';
import {RegistrationComponent} from './account/registration/registration.component';
import {LoginComponent} from './account/login/login.component';
import {ApplicantDetailsComponent} from './admin/application-enrollment-details/applicant-details.component';
import {ProfileComponent} from './account/profile/profile.component';
import {LandingPageComponent} from './landing-page/landing-page.component';
import {ApplicationEnrollmentComponent} from './applicant/application-enrollment/application-enrollment.component';

export const routes: Routes = [
    {path: '', redirectTo: '/home', pathMatch: 'full' },
    {path: 'home', component: LandingPageComponent},
    {path: 'login', component: LoginComponent},
    {path: 'registration', component: RegistrationComponent},
    {path: 'application-enrollment-details', component: ApplicantDetailsComponent},
    {path: 'student-details', component: StudentDetailsComponent},
    {path: 'class-registration', component: ClassRegistrationComponent},
    {path: 'schedule-course', component: ScheduleCourseComponent},
    {path: 'application-enrollment', component: ApplicationEnrollmentComponent},
    {path: 'profile', component: ProfileComponent}
];
