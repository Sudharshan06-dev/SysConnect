import {ChangeDetectorRef, Component} from '@angular/core';
import {Router, RouterLink} from '@angular/router';
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';
import {NgIf} from '@angular/common';
import {label} from '../../../messages/label';
import {errorMessages} from '../../../messages/error';
import {RequestService} from '../../../services/request.service';
import {LocalStorageHelper} from '../../../services/local-storage.service';
import {API_PREFIX} from '../../../environment';
import {SKIP_AUTH_TRUE} from '../../../interceptors/auth.interceptor';
import {ToasterHelper} from '../../../services/toast.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    RouterLink,
    ReactiveFormsModule,
    NgIf
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {

  protected  readonly labels = label.login
  protected readonly  errors = errorMessages.login

  loginForm !: FormGroup

  constructor(private fb: FormBuilder, private apiRequest: RequestService, private cdr: ChangeDetectorRef, private localStorage: LocalStorageHelper, private router: Router, private toastService: ToasterHelper) {
    this.loginForm = this.fb.group({
      username: ['', [Validators.required]],
      password: ['', [Validators.required]]
    })
  }

  login() {
    this.apiRequest.post(API_PREFIX + 'token', this.loginForm.getRawValue(), [SKIP_AUTH_TRUE]).subscribe({
      next: (data: any) => {

        // Handle successful response here
        this.localStorage.storeItem('access_token', data?.access_token)
        this.localStorage.storeItem('user_details', data?.user)
        // Navigate and force change detection


        if(data?.user?.role == 'ADMIN') {
          this.router.navigate(['/admin-dashboard']).then(() => {
            this.cdr.detectChanges();
          });
        } else {
          this.router.navigate(['/application-enrollment']).then(() => {
            this.cdr.detectChanges();
          });
        }
      },

      error: (err: any) => {
        // Handle error response here
        this.toastService.error(err?.error);
      }
    });
  }

}
