import { Component } from '@angular/core';
import {KeyValuePipe, NgForOf, NgIf} from "@angular/common";
import {FormBuilder, FormGroup, ReactiveFormsModule} from "@angular/forms";
import {RouterLink} from "@angular/router";
import {constants} from '../../../messages/constants';

@Component({
  selector: 'app-application-enrollment',
  standalone: true,
  imports: [
    NgIf,
    ReactiveFormsModule,
    RouterLink,
    NgForOf,
    KeyValuePipe
  ],
  templateUrl: './application-enrollment.component.html',
  styleUrl: './application-enrollment.component.css'
})
export class ApplicationEnrollmentComponent {

  applicationEnrollmentForm !: FormGroup

  roleTypes = constants.roleTypes
  majorTypes = constants.majorTypes
  degreeTypes = constants.degreeTypes

  constructor(public fb: FormBuilder) {
  }

  enrollApplication() {
    if (this.applicationEnrollmentForm.valid) {
      console.log(this.applicationEnrollmentForm.value);
      // Do signup logic here
    } else {
      this.applicationEnrollmentForm.markAllAsTouched();
    }
  }

}
