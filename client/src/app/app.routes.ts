import { Routes } from '@angular/router';
import { StudentDetailsComponent } from './student-details/student-details.component';
import { ClassRegistrationComponent } from './class-registration/class-registration.component';
import { ScheduleCourseComponent } from './schedule-course/schedule-course.component';

export const routes: Routes = [
    {path: 'student-details', component: StudentDetailsComponent}, 
    {path: 'class-registration', component: ClassRegistrationComponent}, 
    {path: 'schedule-course', component: ScheduleCourseComponent}
];
