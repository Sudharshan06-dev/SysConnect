import {Component} from '@angular/core';
import {Router, RouterLink} from '@angular/router';
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';
import {KeyValuePipe, NgForOf, NgIf} from '@angular/common';
import {errorMessages} from '../../../messages/error';
import {label} from '../../../messages/label';
import {constants} from '../../../messages/constants';
import {RequestService} from '../../../services/request.service';
import {API_PREFIX} from '../../../environment';
import {ToasterHelper} from '../../../services/toast.service';

@Component({
  selector: 'app-registration',
  standalone: true,
  imports: [
    RouterLink,
    ReactiveFormsModule,
    NgForOf,
    NgIf,
    KeyValuePipe
  ],
  templateUrl: './registration.component.html',
  styleUrl: './registration.component.css'
})
export class RegistrationComponent {

  errors = errorMessages.registration
  labels = label.registration
  roleTypes = constants.roleTypes

  signupForm: FormGroup;

  constructor(private fb: FormBuilder, private apiRequest: RequestService, private toastService: ToasterHelper, private router: Router) {

    this.signupForm = this.fb.group({
      firstname: ['', [Validators.required, Validators.pattern(/^[A-Za-z]+$/)]],
      lastname: ['', [Validators.required, Validators.pattern(/^[A-Za-z]+$/)]],
      username: ['', [Validators.required, Validators.pattern(/^[A-Za-z0-9]+$/)]],
      email: ['', [Validators.required, Validators.email]],
      role: ['', [Validators.required]],
      password: ['', [Validators.required, Validators.minLength(8)]],
      confirmPassword: ['', Validators.required],
    }, {validators: this.passwordMatchValidator});
  }

  passwordMatchValidator(form: FormGroup) {
    const password = form.get('password')?.value;
    const confirmPassword = form.get('confirmPassword')?.value;
    return password === confirmPassword ? null : {mismatch: true};
  }

  submitRegistration() {

    this.apiRequest.post(API_PREFIX + 'register/register-user', this.signupForm.getRawValue()).subscribe({
      next: (data: any) => {
        this.router.navigate(['/login']);
      },

      error: (err: any) => {
        // Handle error response here
        this.toastService.error(err?.error);
      }
    });
  }
}
