package com.aidoctor.controller;

import com.aidoctor.model.Consultation;
import com.aidoctor.model.Patient;
import com.aidoctor.repository.ConsultationRepository;
import com.aidoctor.repository.PatientRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import java.util.List;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "${FRONTEND_ORIGIN:http://localhost:5173}")
public class ConsultationController {
    private final ConsultationRepository consultations;
    private final PatientRepository patients;

    public ConsultationController(ConsultationRepository consultations, PatientRepository patients) {
        this.consultations = consultations;
        this.patients = patients;
    }

    @GetMapping("/patients/{patientId}/consultations")
    public List<Consultation> history(@PathVariable Long patientId) {
        if (!patients.existsById(patientId)) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Patient not found");
        }
        return consultations.findByPatientIdOrderByCreatedAtDesc(patientId);
    }

    @PostMapping("/patients/{patientId}/consultations")
    @ResponseStatus(HttpStatus.CREATED)
    public Consultation create(@PathVariable Long patientId, @Valid @RequestBody Consultation consultation) {
        Patient patient = patients.findById(patientId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Patient not found"));
        consultation.setPatient(patient);
        return consultations.save(consultation);
    }
}
