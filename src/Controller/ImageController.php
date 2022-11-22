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

class ImageController extends AbstractController
{
    #[Route('/image/{id}')]
    public function full(Request $request, int $id, RequestStack $requestStack, HttpClientInterface $apiClient, LoggerInterface $logger): Response
    {
        // if not logged in, redirect to login page
        if ($requestStack->getSession()->get('is_logged_in') !== true) {
            $logger->warning('Not logged in', ['started' => $requestStack->getSession()->isStarted()]);
            return $this->redirectToRoute('app_login_index');
        }

        // call api client
        $imageRequest = $apiClient->request('GET', 'https://diensten.rotterdam.nl/sbmob/api/msb/melding/foto/' . $id, [
            'query' => [],
            'auth_bearer' => $requestStack->getSession()->get('msb_token')
        ]);

        return new Response($imageRequest->getContent(), Response::HTTP_OK, [
            'Content-type' => $imageRequest->getHeaders()['content-type'][0]
        ]);
    }

    #[Route('/thumbnail/{id}')]
    public function thumbnail(Request $request, int $id, RequestStack $requestStack, HttpClientInterface $apiClient, LoggerInterface $logger): Response
    {
        // if not logged in, redirect to login page
        if ($requestStack->getSession()->get('is_logged_in') !== true) {
            $logger->warning('Not logged in', ['started' => $requestStack->getSession()->isStarted()]);
            return $this->redirectToRoute('app_login_index');
        }

        // call api client
        $imageRequest = $apiClient->request('GET', 'https://diensten.rotterdam.nl/sbmob/api/msb/melding/foto/' . $id, [
            'query' => ['thumbnail' => 'true'],
            'auth_bearer' => $requestStack->getSession()->get('msb_token')
        ]);

        return new Response($imageRequest->getContent(), Response::HTTP_OK, [
            'Content-type' => $imageRequest->getHeaders()['content-type'][0]
        ]);
    }
}
