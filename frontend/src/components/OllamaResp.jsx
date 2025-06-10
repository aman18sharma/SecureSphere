import React from 'react';
import './OllamaResp.css';

const OllamaResp = () => {
  return (
    <div className="security-notice">
      <h1 className="security-title">Security Vulnerability Notice</h1>
      <p className="security-subtitle">CVE-2025-41232 - Spring Security Framework</p>

      <div className="security-section">
        <h2 className="section-title">What's the issue?</h2>
        <p className="section-content">
          The CVE-2025-41232 vulnerability affects Spring Security version 5.3 and later, when using AspectJ-based method security annotations on private methods. This means that if an application uses AspectJ-based method security annotations on a private method, it may not correctly enforce authorization checks.
        </p>
      </div>

      <div className="security-section">
        <h2 className="section-title">How does this affect my application?</h2>
        <p className="section-content">
          If your application uses <code>@EnableMethodSecurity(mode=ASPECTJ)</code> and has Spring Security-annotated private methods, you may be vulnerable to authorization bypass attacks. This means that an unauthorized user could potentially invoke the private method without proper authorization.
        </p>
      </div>

      <div className="security-section">
        <h2 className="section-title">What can I do to fix this issue?</h2>
        <p className="section-content">
          To fix this vulnerability, you have a few options:
        </p>
        <ol className="remediation-list">
          <li>
            <strong>Disable AspectJ-based method security:</strong> If you're not using <code>@EnableMethodSecurity(mode=ASPECTJ)</code> or Spring Security-annotated private methods, you don't need to take any action.
          </li>
          <li>
            <strong>Re-evaluate your annotation usage:</strong> Review your application's code and ensure that you're using Spring Security annotations correctly on public methods, rather than private ones.
          </li>
          <li>
            <strong>Upgrade to a fixed version of Spring Security:</strong> If you can't modify your existing code, consider upgrading to a newer version of Spring Security that includes a fix for this vulnerability.
          </li>
        </ol>
      </div>

      <div className="security-section important-notes">
        <h2 className="section-title">Important notes</h2>
        <ul className="notes-list">
          <li>This vulnerability only affects applications using AspectJ-based method security annotations on private methods.</li>
          <li>The severity of this vulnerability is considered <strong>"High"</strong>, which means it has the potential to cause significant harm if exploited.</li>
        </ul>
      </div>

      <div className="security-footer">
        <p>I hope this helps! Let me know if you have any further questions or concerns.</p>
      </div>
    </div>
  );
};

export default OllamaResp;