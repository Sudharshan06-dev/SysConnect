import {Component, ViewEncapsulation} from '@angular/core';
import {KeyValuePipe, NgClass, NgForOf, NgIf} from "@angular/common";
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from "@angular/forms";
import {RouterLink} from "@angular/router";
import {constants} from '../../../messages/constants';
import {ExpansionPanelComponent} from '@progress/kendo-angular-layout';
import {DropDownListComponent} from '@progress/kendo-angular-dropdowns';
import {FileRestrictions, KENDO_UPLOADS} from '@progress/kendo-angular-upload';
import {errorMessages} from '../../../messages/error';
import {LabelComponent} from '@progress/kendo-angular-label';
import {label} from '../../../messages/label';
import {LocalStorageHelper} from '../../../services/local-storage.service';
import {RequestService} from '../../../services/request.service';
import {API_PREFIX} from '../../../environment';
import {ToasterHelper} from '../../../services/toast.service';

@Component({
  selector: 'app-application-enrollment',
  standalone: true,
  encapsulation: ViewEncapsulation.None,
  imports: [
    NgIf,
    ReactiveFormsModule,
    KENDO_UPLOADS,
    RouterLink,
    NgForOf,
    KeyValuePipe,
    ExpansionPanelComponent,
    DropDownListComponent,
    LabelComponent,
    NgClass
  ],
  templateUrl: './application-enrollment.component.html',
  styleUrl: './application-enrollment.component.css'
})
export class ApplicationEnrollmentComponent {

  majorTypes = constants.majorTypes
  degreeTypes = constants.degreeTypes
  errors = errorMessages.application_enrollment
  labels = label.application_enrollment
  buttonLabel = label.buttonLabel

  resumeFile: any
  lorFile : any = [];
  sopFile: any;

  applicationEnrollmentForm !: FormGroup

  fileRestrictions: FileRestrictions = {
    maxFileSize: 10500000,
    minFileSize: 250,
    allowedExtensions: [".jpg", ".png", ".docx", ".svg", ".xls", ".pdf"],
  };

  applicationDetails !: {} | any

  applicationSubmitted : boolean = false

  /******
   Write code logic to get the data from the backend
   *******/
  user = {
    firstname: 'John',
    lastname: 'Doe',
    email: 'john@example.com',
    username: 'johndoe',
    role: 'Student',
    degree: "Masters",
    major: "Computer Science"
  };


  constructor(public fb: FormBuilder, private localStorage: LocalStorageHelper, private apiRequest: RequestService, private toastService: ToasterHelper) {

    this.applicationEnrollmentForm = this.fb.group({
      degree: ['', Validators.required],
      major: ['', Validators.required],
      resume: ['', Validators.required],
      lor: ['', Validators.required],
      sop: ['', Validators.required]
    });

    this.getApplicantDetails()
  }

  getApplicantDetails() {
    let user_id = this.localStorage.getItem('user_details')?.user_id
    this.apiRequest.post(API_PREFIX + 'applicant/application-details', {user_id}).subscribe({
      next : (data : any) => {
        this.applicationDetails = {...this.localStorage.getItem('user_details'), ...data};
      },
      error: () => {
        this.applicationDetails = {}
      }
    })
  }

  onFileSelect(event: any, fileType: 'resume' | 'lor' | 'sop') {
    const selectedFiles: File[] = event.files.map((f: any) => f.rawFile);
    const control = this.applicationEnrollmentForm.get(fileType);

    if (!control) return;

    // MULTIPLE files for LOR
    /*if (fileType === 'lor') {
      const existing = control.value || [];
      control.setValue([...existing, ...selectedFiles]);
    } else {
      // SINGLE file for SOP/Resume
      control.setValue(selectedFiles[0]);
    }*/

    control.setValue(selectedFiles[0]);
  }


  /**
   * Multiple files not working properly while deleting them
   * **/
  removeFile(fileType: 'resume' | 'lor' | 'sop', fileToRemove?: File) {
    const control = this.applicationEnrollmentForm.get(fileType);
    if (!control) return;

    if (fileType === 'lor') {
      // Get current files array
      const files = [...(control.value || [])];

      // Only proceed if we have files and a file to remove
      if (files.length && fileToRemove) {
        const updatedFiles = files.filter((file: File) =>
          // You might need a different comparison depending on your use case
          file.name !== fileToRemove.name && file.type !== fileToRemove.type
        );

        // Set the new array without the removed file
        control.setValue(updatedFiles);

        // Ensure Angular recognizes the change
        control.markAsDirty();
        control.markAsTouched();
        control.updateValueAndValidity({ onlySelf: false, emitEvent: true });
      }
    } else {
      // For single file types
      control.setValue(null);
      control.updateValueAndValidity();
    }
  }



  clearForm() {
    this.applicationEnrollmentForm.reset();
  }

  enrollApplication() {
    if (this.applicationEnrollmentForm.invalid) return;

    const rawData = {
      ...this.applicationEnrollmentForm.getRawValue(),
      ...this.applicationDetails
    };

    console.log(rawData)

    //Degree and Major not working here

    const formData = new FormData();

    Object.entries(rawData).forEach(([key, value]) => {
      if (Array.isArray(value) && value.length > 0 && value[0] instanceof File) {
        // For file arrays, use the same key name for each file
        // This will create an array on the server side with the same key
        let files: any = []

        value.forEach((file) => {
          files.push(file);
        });

        formData.append(key, files)
      } else if (value instanceof File) {
        formData.append(key, value);
      } else if (value !== null && value !== undefined) {
        formData.append(key, value.toString());
      }
    });

    // Now use formData instead of rawData for the API request
    this.apiRequest.fileRequest(API_PREFIX + 'applicant/enroll-application', formData).subscribe({
      next: (response: any) => {
        this.toastService.success(response);
        this.applicationSubmitted = true;
      },
      error: (err: any) => {
        this.toastService.error(err?.error);
        this.applicationSubmitted = false;
      }
    });
  }

  previewFile(s3Key: string) {

    let s3_url = 'applications/' + this.applicationDetails.reference_number + '/' + s3Key;

    this.apiRequest.get(API_PREFIX + `applicant/get-file/${s3_url}`, {responseType: 'blob', observe: 'response'}).subscribe((response : any) => {
      const blob = new Blob([response.body!], {type: response.headers.get('Content-Type')!});
      const url = window.URL.createObjectURL(blob);

      // Open in new tab for preview
      const newTab = window.open();
      if (newTab) {
        newTab.location.href = url;
      } else {
        alert('Popup blocked! Please allow popups for this site.');
      }

      // Optional: Revoke URL after some time (e.g., 5 minutes)
      setTimeout(() => {
        window.URL.revokeObjectURL(url);
      }, 300000);
    });

  }

  downloadFile(s3Key: string) {

    let s3_url = 'applications/' + this.applicationDetails.reference_number + '/' + s3Key;

    this.apiRequest.get(API_PREFIX + `applicant/get-file/${s3_url}`, {responseType: 'blob', observe: 'response'}).subscribe((response : any) => {
      // Create download link
      const blob = new Blob([response.body!], {type: response.headers.get('Content-Type')!});
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = s3Key.split('/').pop()!;
      link.click();
      window.URL.revokeObjectURL(url);
    });
  }

}
