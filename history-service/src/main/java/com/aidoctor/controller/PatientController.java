package com.aidoctor.controller;

import com.aidoctor.model.Patient;
import com.aidoctor.repository.PatientRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/patients")
@CrossOrigin(origins = "${FRONTEND_ORIGIN:http://localhost:5173}")
public class PatientController {
    private final PatientRepository patients;

    public PatientController(PatientRepository patients) {
        this.patients = patients;
    }

    @GetMapping
    public List<Patient> list() { return patients.findAll(); }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Patient create(@Valid @RequestBody Patient patient) {
        return patients.save(patient);
    }
}
