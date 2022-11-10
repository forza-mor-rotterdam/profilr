<?php

declare(strict_types=1);

namespace App\Controller;

use Psr\Log\LoggerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\RequestStack;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Contracts\HttpClient\HttpClientInterface;

class LoginController extends AbstractController
{
    #[Route('/login', name: 'app_login_index')]
    public function index(Request $request, RequestStack $requestStack, HttpClientInterface $apiClient, LoggerInterface $logger): Response
    {
        // variabel for holding login errors
        $error = null;

        // if the submit form is submitted
        if ($request->isMethod('POST')) {
            
            // check credentials against api
            $loginResponse = $apiClient->request('POST', 'https://diensten.rotterdam.nl/sbmob/api/login', [
                'body' => [
                    'uid' => $request->request->get('_username'),
                    'pwd' => $request->request->get('_password'),
                ]
            ])->toArray();

            // if success, save the received token and redirect user to incidents index page
            if ($loginResponse['success'] === true) {
            
                $requestStack->getSession()->set('msb_token', $loginResponse['result']);
                $requestStack->getSession()->set('is_logged_in', true);

                return $this->redirectToRoute('app_filter_index');
            } else {
                $requestStack->getSession()->set('is_logged_in', false);

                // login failed, set error message for the template
                $error = 'invalid_username_or_password';
            }
        }

        // render template
        return $this->render('login/index.html.twig', [
            'last_username' => $request->request->get('_username', ''),
            'error' => $error
        ]);
    }
}
